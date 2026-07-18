%global debug_package %{nil}
%global _binary_payload w22T0.zstdio
%global app_id io.github.dweymouth.supersonic

Name:           supersonic
Version:        0.22.0
Release:        2%{?dist}
Summary:        Cross-platform desktop client for self-hosted music servers

License:        GPL-3.0-or-later
URL:            https://github.com/dweymouth/supersonic
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  golang >= 1.24
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
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
export CGO_ENABLED=1
export CGO_CFLAGS="${CFLAGS}"
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
export GOTOOLCHAIN=local

go build -v -mod=mod -trimpath -buildmode=pie -ldflags="-s -w" -o %{name} .

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
appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%post
%{_bindir}/update-desktop-database &> /dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &> /dev/null || :

%postun
%{_bindir}/update-desktop-database &> /dev/null || :
%{_bindir}/gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &> /dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{app_id}.png
%{_datadir}/icons/hicolor/256x256/apps/%{app_id}.png
%{_datadir}/icons/hicolor/512x512/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu Jul 13 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.22.0-2
- The most notable change in 0.22.0 is the migration to Fyne 2.8. For Linux users, this adds full Wayland support, auto-selecting X11 or Wayland at startup from the same release binary. Building from source and specifying `-tags wayland` is no longer needed. It also fixes a few bugs that have impacted the `-tags wayland` builds.
- #909 IPC endpoint for getting the current track/radio station
- #910 Support for the OpenSubsonic playbackReport extension
- #955 "All Tracks" option on the Startup page
- Cover art support for internet radio stations
- Updated Polish, Spanish, Greek, Turkish, and French translations
- #54 Migrate to Fyne 2.8, adding Wayland support
- #958 Match window border color to app theme rather than OS theme
- #803 Artist biography text now scrolls instead of being truncated
- #560 UI freeze after switching workspaces on Wayland
- #823 Segfault when clicking the tray icon on Wayland
- #899 Crash/freeze when system keyring unlock dialog blocked the main event loop on startup
- #740 Race condition when using an alternate hostname caused 401 auth errors
- #917 UI scale setting not applied correctly when using a non-English language
- #931 DLNA cast DIDL-Lite metadata missing artist, album, cover art, and <res> audio attributes
- Stale cover art and Now Playing background persisting on tracks without art
- Autoplay (similar songs) incorrectly enqueuing tracks while a radio station is playing
- Full Changelog: https://github.com/dweymouth/supersonic/compare/v0.21.1...v0.22.0
