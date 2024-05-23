{
    description = "p8 plots";
    inputs = {
        nixpkgs.url = "nixpkgs/nixos-unstable";
    };
    outputs = { self, nixpkgs }: let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
    in {
        devShells.${system}.default = pkgs.mkShell {
            packages = with pkgs; [
                (python311.withPackages (py: with py; [
                    matplotlib
                ]))
            sqlite-interactive
            ];
        };
    };
}
