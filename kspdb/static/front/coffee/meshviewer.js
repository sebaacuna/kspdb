(function() {
  $(document).ready(function() {
    var $view, camera, render, renderer, scene;
    $view = $(".js-meshview");
    if (!$view.length) {
      return;
    }
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, $view.width() / $view.height(), 0.1, 1000);
    camera.position.z = 5;
    renderer = new THREE.WebGLRenderer();
    renderer.setSize($view.width(), $view.height());
    $view.append(renderer.domElement);
    scene = null;
    render = function() {
      requestAnimationFrame(render);
      if (scene) {
        scene.rotation.x += 0.01;
        scene.rotation.z += 0.01;
        return renderer.render(scene, camera);
      }
    };
    render();
    return window.showMesh = function(data) {
      var copy, cpyTrio, geometry, i, material, mesh, srcTrio, wireframe, _i, _len, _ref;
      material = new THREE.MeshBasicMaterial({
        color: 0x00ffff
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
      copy(data.vertices, THREE.Vector3, geometry.vertices);
      copy(data.faces, THREE.Face3, geometry.faces);
      _ref = data.faceVertexUvs[0];
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
        srcTrio = _ref[i];
        cpyTrio = [];
        copy(srcTrio, THREE.Vector2, cpyTrio);
        geometry.faceVertexUvs[0].push(cpyTrio);
      }
      mesh = new THREE.Mesh(geometry, material);
      wireframe = new THREE.WireframeHelper(mesh, 0x00ff00);
      scene = new THREE.Scene();
      return scene.add(wireframe);
    };
  });

}).call(this);
