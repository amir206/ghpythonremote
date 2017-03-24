from os import path
from ghpythonremote import PythonToGrasshopperRemote


if __name__ == '__main__':
    ROOT = path.abspath(path.join(path.curdir, '..'))
    rhino_file_path = path.join(ROOT, 'examples', 'curves.3dm')
    rpyc_server_py = path.join(ROOT, 'ghcompservice.py')
    with PythonToGrasshopperRemote(None, rpyc_server_py, timeout=60) as py2gh:
        rghcomp = py2gh.gh_remote_components
        rgh = py2gh.connection
        Rhino = rgh.modules.Rhino
        rs = rgh.modules.rhinoscriptsyntax

        readopt = Rhino.FileIO.FileReadOptions()
        readopt.BatchMode = True
        Rhino.RhinoDoc.ReadFile(rhino_file_path, readopt)  # Or pass in a first argument to py2gh to open a file

        type_curve = Rhino.DocObjects.ObjectType.Curve
        curves = Rhino.RhinoDoc.ActiveDoc.Objects.FindByObjectType(type_curve)
        curves_id = tuple(c.Id for c in curves)  # rhinoscriptsyntax doesn't like mutable objects through the connection
        gh_curves = rs.coerceguidlist(curves_id)
        area = rghcomp('Area', is_cluster_component=False)
        print(sum(area(gh_curves)[0]))
