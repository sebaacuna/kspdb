from itertools import groupby
import logging
import re
from kspdb.apps.main.models import Part, Resource

logger = logging.getLogger(__name__)


class BaseObj(dict):
    def __init__(self):
        self.attributes = {}


class CraftObj(BaseObj):
    def __init__(self):
        super().__init__()
        self.parts = []

    def stats(self):
        resources = {}
        for r in Resource.objects.all():
            resources[r.name] = r

        resmass = 0
        drymass = 0
        crewcapacity = 0
        res = {}
        for p in self.parts:
            drymass += float(p.model.obj['mass'])
            crewcapacity += int(p.model.obj.get('CrewCapacity',0))
            for rtype, amount in p.resources.items():
                res[rtype] = res.get(rtype, 0) + amount
                resmass += resources[rtype].density * amount

        return (
            ("parts", len(self.parts)),
            ("stages", sum(1 for _ in self.stages())),
            ("drymass", drymass),
            ("totalmass", drymass + resmass),
            ("crewcapacity", crewcapacity)
        ) + tuple(res.items())

    def stages(self):
        sortkey = lambda p: "{sepI}.{istg}.{dstg}".format(**p)
        groupkey = lambda p: p['sepI']
        return [
            (k, list(g))
            for k, g in groupby(
                sorted(self.parts, key=sortkey),
                groupkey)]


class PartObj(BaseObj):
    def __init__(self):
        self.resources = {}


###########
# Parsers #
###########
class Stop(Exception):
    pass


class BaseParser:
    obj_class = BaseObj
    root = None
    handlers = (
        (re.compile(r'//'), 'comment'),
        (re.compile(r'(.+)=(.+)'), 'attribute'),
        (re.compile(r'{'), 'start'),
        (re.compile(r'}'), 'stop'),
        (re.compile(r'(\w+)'), 'section'),
    )

    def __init__(self, lines, root=None):
        try:
            self.lines = iter(lines.splitlines())
        except AttributeError:
            assert hasattr(lines, '__next__')
            self.lines = lines

        self.content = ''

        if root is not None:
            self.root = root

    def parse(self):
        self.obj = self.obj_class()
        for line in self.lines:
            self.content += line + "\n"
            for regex, handler in self.handlers:
                match = regex.search(line)
                if match:
                    try:
                        args = match.groups()
                    except AttributeError:
                        args = ()

                    try:
                        getattr(self, handler)(*args)
                        break
                    except Stop:
                        return self.obj

        return self.obj

    def comment(self):
        pass

    def attribute(self, name, value):
        self.obj[name.strip()] = value.strip()

    def start(self):
        pass

    def stop(self):
        raise Stop()

    def section(self, section):
        parser = BaseParser(self.lines)
        secobj = parser.parse()
        self.content += parser.content
        if section == self.root:
            self.obj = secobj
        return secobj


class CraftParser(BaseParser):
    obj_class = CraftObj

    @staticmethod
    def model_parser(craft):
        parser = CraftParser(craft.data)
        return parser

    def section(self, name):
        if name == 'PART':
            parser = PartParser(self.lines)
            part = parser.parse()
            self.obj.parts.append(part)
            self.content += parser.content
            return part
        else:
            return super().section(name)


class PartParser(BaseParser):
    obj_class = PartObj
    root = 'PART'

    def section(self, name):
        secobj = super().section(name)
        if name == 'RESOURCE':
            res = secobj['name']
            amount = float(secobj['amount'])
            try:
                self.obj.resources[res] += amount
            except KeyError:
                self.obj.resources[res] = amount
        return secobj

    def stop(self):
        part_name, serial = self.obj['part'].split('_')
        part_name = part_name.replace(".", "_")

        self.obj['partName'] = part_name
        self.obj['serial'] = serial
        try:
            self.obj.model = Part.objects.get(partName=part_name)
        except Part.DoesNotExist:
            self.obj.model = None
            logger.warn("Part not found: {}".format(part_name))
        raise Stop()
