Name:           supersonic
Version:        0.22.0
Release:        1%{?dist}
Summary:        Cross-platform desktop client for self-hosted music servers

License:        GPL-3.0-or-later
URL:            https://github.com/dweymouth/supersonic
Source0:        %{url}/archive/refs/tags/v%{version}/supersonic-%{version}.tar.gz

BuildRequires:  golang >= 1.21
BuildRequires:  make
BuildRequires:  git
BuildRequires:  desktop-file-utils
BuildRequires:  mpv-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXi-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libXxf86vm-devel

Obsoletes:      supersonic-desktop < %{version}-%{release}
Provides:       supersonic-desktop = %{version}-%{release}

%description
A lightweight and full-featured cross-platform desktop client for self-hosted music servers

%prep
%autosetup -n supersonic-%{version}

%build
export GOFLAGS=-mod=mod
make build

%install
install -Dm755 supersonic %{buildroot}%{_bindir}/%{name}

install -Dm644 res/supersonic-desktop.desktop \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i -e '/^Path=/d' \
       -e "s/^Exec=.*/Exec=%{name}/" \
       -e "s/^Icon=.*/Icon=%{name}/" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

for size in 128 256 512; do
  install -Dm644 res/appicon-${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Thu Jul 16 2026 coffeeicus coffeelover@coffeelover.uk - 0.22.0-1
- Rename package from supersonic-desktop to supersonic
- Rely on automatic ELF dependency detection instead of manual Requires
