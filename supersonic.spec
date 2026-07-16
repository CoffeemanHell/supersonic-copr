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
- The most notable change in 0.22.0 is the migration to Fyne 2.8. For Linux users, this adds full Wayland support, auto-selecting X11 or Wayland at startup from the same release binary. Building from source and specifying `-tags wayland` is no longer needed. It also fixes a few bugs that have impacted the `-tags wayland` builds.
- [#909](https://github.com/dweymouth/supersonic/issues/909) IPC endpoint for getting the current track/radio station
- [#910](https://github.com/dweymouth/supersonic/pull/910) Support for the OpenSubsonic `playbackReport` extension
- [#955](https://github.com/dweymouth/supersonic/pull/955) "All Tracks" option on the Startup page
- Cover art support for internet radio stations
- Updated Polish, Spanish, Greek, Turkish, and French translations
- [#54](https://github.com/dweymouth/supersonic/issues/54) Migrate to Fyne 2.8, adding Wayland support
- [#958](https://github.com/dweymouth/supersonic/pull/958) Match window border color to app theme rather than OS theme
- [#803](https://github.com/dweymouth/supersonic/issues/803) Artist biography text now scrolls instead of being truncated
- [#560](https://github.com/dweymouth/supersonic/issues/560) UI freeze after switching workspaces on Wayland
- [#823](https://github.com/dweymouth/supersonic/issues/823) Segfault when clicking the tray icon on Wayland
- [#899](https://github.com/dweymouth/supersonic/issues/899) Crash/freeze when system keyring unlock dialog blocked the main event loop on startup
- [#740](https://github.com/dweymouth/supersonic/issues/740) Race condition when using an alternate hostname caused 401 auth errors
- [#917](https://github.com/dweymouth/supersonic/issues/917) UI scale setting not applied correctly when using a non-English language
- [#931](https://github.com/dweymouth/supersonic/issues/931) DLNA cast DIDL-Lite metadata missing artist, album, cover art, and `<res>` audio attributes
- Stale cover art and Now Playing background persisting on tracks without art
- Autoplay (similar songs) incorrectly enqueuing tracks while a radio station is playing
- @ocelotsloth made their first contribution in https://github.com/dweymouth/supersonic/pull/900
- @tdakkota made their first contribution in https://github.com/dweymouth/supersonic/pull/911
- @oakrotka made their first contribution in https://github.com/dweymouth/supersonic/pull/918
- @Promax1113 made their first contribution in https://github.com/dweymouth/supersonic/pull/923
- @ilias-sp made their first contribution in https://github.com/dweymouth/supersonic/pull/926
- @andrewdunndev made their first contribution in https://github.com/dweymouth/supersonic/pull/934
- @TheProzin made their first contribution in https://github.com/dweymouth/supersonic/pull/942
- @lfzawacki made their first contribution in https://github.com/dweymouth/supersonic/pull/946
- @belzebub40k made their first contribution in https://github.com/dweymouth/supersonic/pull/950
- @Golbinex made their first contribution in https://github.com/dweymouth/supersonic/pull/955
- @Inevitabby made their first contribution in https://github.com/dweymouth/supersonic/pull/957
- @tofuliang made their first contribution in https://github.com/dweymouth/supersonic/pull/966
- Full Changelog: https://github.com/dweymouth/supersonic/compare/v0.21.1...v0.22.0


* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.21.1-1
