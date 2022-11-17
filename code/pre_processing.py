"""
Script for converting gmsh files to dolfin format
using cardiac geometries

https://computationalphysiology.github.io/cardiac_geometries/

"""
import typing
from pathlib import Path

import cardiac_geometries
import config
from cardiac_geometries.geometry import Geometry
from cardiac_geometries.geometry import H5Path

schema = {
    "mesh": H5Path(
        h5group="/mesh",
        is_mesh=True,
    ),
    "ffun": H5Path(
        h5group="/ffun",
        is_meshfunction=True,
        dim=2,
        mesh_key="mesh",
    ),
    "markers": H5Path(
        h5group="/markers",
        is_dolfin=False,
    ),
}


def convert_mesh(
    msh_file: typing.Union[Path, str],
    outfile: typing.Union[Path, str],
) -> None:

    print("Converting 'msh' file to dolfin xdmf format")
    geometry = cardiac_geometries.gmsh2dolfin(msh_file, unlink=True)

    geo = Geometry(
        mesh=geometry.mesh,
        markers=geometry.markers,
        ffun=geometry.marker_functions.ffun,
        schema=schema,
    )

    geo.save(outfile)
    print(f"Saved to {outfile}")


def main() -> int:
    for heart_nr in [1, 2]:
        msh_file = config.get_msh_path(heart_nr=heart_nr)
        outfile = config.get_h5_path(heart_nr=heart_nr)
        convert_mesh(msh_file=msh_file, outfile=outfile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
