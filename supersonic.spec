%global _binary_payload w22T0.zstdio
%global app_id io.github.dweymouth.supersonic

Name:           supersonic
Version:        0.22.1
Release:        1%{?dist}
Summary:        Cross-platform desktop client for self-hosted music servers

License:        GPL-3.0-or-later
URL:            https://github.com/supersonic-app/supersonic
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  golang >= 1.24
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(mpv)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(xxf86vm)

Requires:       hicolor-icon-theme

Obsoletes:      supersonic-desktop < %{version}-%{release}
Provides:       supersonic-desktop = %{version}-%{release}

%description
A lightweight and full-featured cross-platform desktop client for
self-hosted music servers.

%prep
%autosetup -n %{name}-%{version}

sed -i 's|<id>io.github.supersonic-app.supersonic</id>|<id>%{app_id}</id>|' res/io.github.dweymouth.supersonic.appdata.xml

%build
export CGO_ENABLED=1
export CGO_CFLAGS="${CFLAGS}"
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
export GOTOOLCHAIN=local

go build -v -mod=mod -buildmode=pie -o %{name} .

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cp res/supersonic-desktop.desktop res/%{app_id}.desktop
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --remove-key="Path" \
  --set-key="Exec" --set-value="%{name}" \
  --set-key="Icon" --set-value="%{app_id}" \
  res/%{app_id}.desktop

for size in 128 256 512; do
  install -Dm644 res/appicon-${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{app_id}.png
done

install -Dm644 res/io.github.dweymouth.supersonic.appdata.xml \
  %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sun Aug 09 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.22.1-1
- 0.22.1 brings several Wayland fixes and a few other fixes and enhancements
- Full Changelog: https://github.com/supersonic-app/supersonic/compare/v0.22.0...v0.22.1

* Mon Jul 13 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.22.0-3
- The most notable change in 0.22.0 is the migration to Fyne 2.8.
- For Linux users, this adds full Wayland support, auto-selecting
- X11 or Wayland at startup from the same release binary.
- Full Changelog: https://github.com/supersonic-app/supersonic/compare/v0.21.1...v0.22.0
