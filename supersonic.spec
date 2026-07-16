%global debug_package %{nil}
%global _binary_payload w22T0.zstdio

Name:           supersonic
Version:        0.22.0
Release:        1%{?dist}
Summary:        Cross-platform desktop client for self-hosted music servers

License:        GPL-3.0-or-later
URL:            https://github.com/dweymouth/supersonic
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.21
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconf-pkg-config
BuildRequires:  mpv-devel
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXi-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libXxf86vm-devel

Requires:       hicolor-icon-theme

Obsoletes:      supersonic-desktop < %{version}-%{release}
Provides:       supersonic-desktop = %{version}-%{release}

%description
A lightweight and full-featured cross-platform desktop client for self-hosted music servers.

%prep
%autosetup -n %{name}-%{version}

%build
%set_build_flags

export CGO_ENABLED=1

export GOAMD64=v2
export CFLAGS="%{optflags} -march=x86-64-v2"
export CXXFLAGS="%{optflags} -march=x86-64-v2"

go build -v -mod=mod -trimpath -buildmode=pie -tags="wayland" -ldflags="-s -w" -o %{name} .

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

cp res/supersonic-desktop.desktop res/%{name}.desktop
mkdir -p %{buildroot}%{_datadir}/applications

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --remove-key="Path" \
  --set-key="Exec" --set-value="%{name}" \
  --set-key="Icon" --set-value="%{name}" \
  res/%{name}.desktop

for size in 128 256 512; do
  install -Dm644 res/appicon-${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.22.0-1
