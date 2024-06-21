{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    buildInputs = with pkgs; [ 
      blender
      f3d
      python311Packages.numpy 
      python311Packages.pillow 
      python311Packages.trimesh 
      python311Packages.qrcode 
	];
}
