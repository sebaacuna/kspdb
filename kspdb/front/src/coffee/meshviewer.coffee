$(document).ready ()->
    $view = $(".js-meshview")
    return unless $view.length

    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera 75, ($view.width() / $view.height()), 0.1, 1000
    camera.position.z = 5

    renderer = new THREE.WebGLRenderer()
    renderer.setSize $view.width(), $view.height()
    $view.append renderer.domElement

    scene = null

    render = ()->
        requestAnimationFrame render
        if scene
            scene.rotation.x += 0.01
            scene.rotation.z += 0.01
            renderer.render scene, camera
    render()

    window.showMesh = (data)->
        material = new THREE.MeshBasicMaterial color: 0x00ffff
        geometry = new THREE.Geometry()

        copy = (srcArray, cpyClass, destArray) ->
            for src in srcArray
                cpy = new cpyClass
                for fld of src
                    cpy[fld] = src[fld]
                destArray.push cpy

        copy data.vertices, THREE.Vector3, geometry.vertices
        copy data.faces, THREE.Face3, geometry.faces

        for srcTrio, i in data.faceVertexUvs[0]
            cpyTrio = []
            copy srcTrio, THREE.Vector2, cpyTrio
            geometry.faceVertexUvs[0].push cpyTrio

        mesh = new THREE.Mesh geometry, material
        wireframe = new THREE.WireframeHelper mesh, 0x00ff00

        scene = new THREE.Scene()
        # scene.add mesh
        scene.add wireframe
