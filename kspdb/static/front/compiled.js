(function() {
  $(document).on('click', '.js-action-partmesh', function(event) {
    var partId;
    console.log("clicked");
    partId = $(event.currentTarget).attr("data-part");
    return $.get("/part_mesh/" + partId, function(data) {
      $('.js-meshdebug').html(JSON.stringify(data));
      return window.showMesh(data);
    });
  });

}).call(this);
;(function() {
  $(document).ready(function() {
    var $view, camera, controls, convertObj, meshFromObj, render, renderer, scene;
    $view = $(".js-meshview");
    if (!$view.length) {
      return;
    }
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, $view.width() / $view.height(), 0.1, 1000);
    camera.position.z = 5;
    renderer = new THREE.WebGLRenderer({
      alpha: true
    });
    renderer.setSize($view.width(), $view.height());
    $view.append(renderer.domElement);
    controls = new THREE.TrackballControls(camera, $view[0]);
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;
    controls.keys = [65, 83, 68];
    scene = null;
    render = function() {
      requestAnimationFrame(render);
      controls.update();
      if (scene) {
        scene.rotation.x += 0.001;
        scene.rotation.y += 0.01;
        return renderer.render(scene, camera);
      }
    };
    render();
    window.showMesh = function(obj) {
      var threeObj;
      scene = new THREE.Scene();
      console.log(obj);
      threeObj = convertObj(obj);
      return scene.add(threeObj);
    };
    convertObj = function(obj) {
      var child, threeObj, _i, _len, _ref;
      threeObj = new THREE.Object3D();
      if (obj.geom) {
        threeObj.add(meshFromObj(obj));
      }
      if (obj.children) {
        _ref = obj.children;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          child = _ref[_i];
          threeObj.add(convertObj(child));
        }
      }
      return threeObj;
    };
    return meshFromObj = function(obj) {
      var copy, geometry, material;
      material = new THREE.MeshBasicMaterial({
        color: randomColor({
          hue: 'blue'
        })
      });
      geometry = new THREE.Geometry();
      copy = function(srcArray, cpyClass, destArray) {
        var cpy, fld, src, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = srcArray.length; _i < _len; _i++) {
          src = srcArray[_i];
          cpy = new cpyClass;
          for (fld in src) {
            cpy[fld] = src[fld];
          }
          _results.push(destArray.push(cpy));
        }
        return _results;
      };
      copy(obj.geom.vertices, THREE.Vector3, geometry.vertices);
      copy(obj.geom.faces, THREE.Face3, geometry.faces);
      return new THREE.Mesh(geometry, material);
    };
  });

}).call(this);
