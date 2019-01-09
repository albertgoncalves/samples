{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [ python36
                    python36Packages.selenium
                    python36Packages.beautifulsoup4
                    python36Packages.flake8
                    wget
                  ];
    shellHook = ''
        if [ $(uname -s) = "Darwin" ]; then
            os="mac"
        else
            os="linux"
        fi

        chromedriver_zip=chromedriver_"$os"64.zip
        chromedriver_path="chromedriver"

        if [ ! -e $chromedriver_zip ]; then
            wget "https://chromedriver.storage.googleapis.com/2.45/$chromedriver_zip"
        fi

        if [ ! -e $chromedriver_path ]; then
            unzip $chromedriver_zip -d ./
        fi

        export chromedriver_path=$(pwd)/$chromedriver_path
        alias flake8="flake8 --ignore E124,E128,E201,E203,E241,W503"
        alias ls='ls --color=auto'
        alias ll='ls -al'
    '';
}
