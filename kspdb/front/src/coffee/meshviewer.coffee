$(document).ready ()->
    $view = $(".js-meshview")
    return unless $view.length

    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera 75, ($view.width() / $view.height()), 0.1, 1000
    camera.position.z = 5

    renderer = new THREE.WebGLRenderer alpha: true
    renderer.setSize $view.width(), $view.height()
    $view.append renderer.domElement

    controls = new THREE.TrackballControls camera, $view[0]

    controls.rotateSpeed = 1.0
    controls.zoomSpeed = 1.2
    controls.panSpeed = 0.8

    controls.noZoom = false
    controls.noPan = false

    controls.staticMoving = true
    controls.dynamicDampingFactor = 0.3

    controls.keys = [ 65, 83, 68 ]

    scene = null

    render = ()->
        requestAnimationFrame render
        controls.update()
        if scene
            scene.rotation.x += 0.001
            scene.rotation.y += 0.01
            renderer.render scene, camera


    # controls.addEventListener 'change', render
    render()

    window.showMesh = (obj)->
        scene = new THREE.Scene()
        console.log obj

        threeObj = convertObj obj
        scene.add threeObj

    convertObj = (obj)->
        threeObj = new THREE.Object3D()

        if obj.geom
            threeObj.add meshFromObj(obj)

        if obj.children
            for child in obj.children
                threeObj.add convertObj(child)

        return threeObj

    meshFromObj = (obj)->
        material = new THREE.MeshBasicMaterial color: randomColor(hue:'blue')
        geometry = new THREE.Geometry()

        copy = (srcArray, cpyClass, destArray) ->
            for src in srcArray
                cpy = new cpyClass
                for fld of src
                    cpy[fld] = src[fld]
                destArray.push cpy

        copy obj.geom.vertices, THREE.Vector3, geometry.vertices
        copy obj.geom.faces, THREE.Face3, geometry.faces

        # for srcTrio, i in data.faceVertexUvs[0]
        #     cpyTrio = []
        #     copy srcTrio, THREE.Vector2, cpyTrio
        #     geometry.faceVertexUvs[0].push cpyTrio

        new THREE.Mesh geometry, material

        # axisHelper = new THREE.AxisHelper 2
        # scene.add axisHelper
