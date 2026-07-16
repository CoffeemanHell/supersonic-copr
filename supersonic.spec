%global debug_package %{nil}
%global _binary_payload w22T0.zstdio
%global app_id io.github.dweymouth.supersonic

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
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme

Obsoletes:      supersonic-desktop < %{version}-%{release}
Provides:       supersonic-desktop = %{version}-%{release}

%description
A lightweight and full-featured cross-platform desktop client for self-hosted music servers.

%prep
%autosetup -n %{name}-%{version}

cat > %{app_id}.metainfo.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2023 anarcat <anarcat@debian.org> -->
<component type="desktop-application">
  <id>io.github.dweymouth.supersonic</id>
  <metadata_license>FSFAP</metadata_license>
  <project_license>GPL-3.0+</project_license>
  <name>Supersonic</name>
  <developer id="github.com/dweymouth">
    <name>Drew Weymouth</name>
  </developer>
  <summary> A lightweight cross-platform desktop client for Subsonic and Jellyfin music servers</summary>
  <content_rating type="oars-1.0">
    <content_attribute id="social-audio">intense</content_attribute>
  </content_rating>

  <description>
    <p>
      A lightweight cross-platform desktop client for Subsonic and Jellyfin music
      servers.
    </p>

    <p>
      Features:
    </p>
    <ul>
      <li>Fast, lightweight, native UI, with infinite scrolling</li>
      <li>Light and Dark themes, with optional auto theme switching</li>
      <li>High-quality gapless audio playback powered by MPV, with optional audio exclusive mode</li>
      <li>ReplayGain support (depends on files being tagged on server)</li>
      <li>MPRIS and Mac OS media center integration</li>
      <li>Scrobble plays to server, with configurable criteria</li>
      <li>Multi-server support</li>
      <li>Primary and alternate server hostnames, e.g. for internal and external URLs</li>
      <li>Set filters in albums browsing view</li>
      <li>Sort tracklist views by column and configure visible tracklist columns</li>
      <li>Set/unset favorite and browse by favorite albums, artists, and songs</li>
      <li>Shuffle and repeat playback modes (partial; shuffle album, playlist, artist radio, random songs)</li>
    </ul>
  </description>

  <categories>
    <category>Audio</category>
  </categories>

  <launchable type="desktop-id">io.github.dweymouth.supersonic.desktop</launchable>

  <url type="homepage">https://github.com/dweymouth/supersonic</url>
  <url type="bugtracker">https://github.com/dweymouth/supersonic/issues</url>
  <screenshots>
    <screenshot type="default">
      <caption>The options dialog</caption>
      <image>https://raw.githubusercontent.com/dweymouth/supersonic/main/res/screenshots/AlbumsView.png</image>
    </screenshot>
    <screenshot>
      <image>https://raw.githubusercontent.com/dweymouth/supersonic/main/res/screenshots/AlbumView.png</image>
    </screenshot>
    <screenshot>
      <image>https://raw.githubusercontent.com/dweymouth/supersonic/main/res/screenshots/ArtistView.png</image>
    </screenshot>
    <screenshot>
      <image>https://raw.githubusercontent.com/dweymouth/supersonic/main/res/screenshots/FavoriteSongsView.png</image>
    </screenshot>
  </screenshots>

 <releases>
  <release version="0.21.1" date="2026-04-07">
   <description></description>
  </release>
  <release version="0.21.0" date="2026-03-12">
   <description/>
  </release>
  <release version="0.20.1" date="2026-01-31">
   <description/>
  </release>
  <release version="0.20.0" date="2026-01-11">
   <description/>
  </release>
  <release version="0.19.0" date="2025-10-30">
   <description/>
  </release>
  <release version="0.18.1" date="2025-09-15">
   <description/>
  </release>
  <release version="0.18.0" date="2025-08-12">
   <description/>
  </release>
  <release version="0.17.0" date="2025-07-16">
   <description/>
  </release>
  <release version="0.16.0" date="2025-06-17">
   <description/>
  </release>
  <release version="0.15.2" date="2025-04-25">
   <description/>
  </release>
  <release version="0.15.1" date="2025-04-07">
   <description/>
  </release>
  <release version="0.15.0" date="2025-04-07">
   <description/>
  </release>
  <release version="0.14.0" date="2025-02-24">
   <description/>
  </release>
  <release version="0.13.2" date="2024-12-22">
   <description/>
  </release>
  <release version="0.13.1" date="2024-08-20">
   <description/>
  </release>
  <release version="0.13.0" date="2024-07-31">
   <description/>
  </release>
  <release version="0.12.0" date="2024-07-01">
   <description/>
  </release>
  <release version="0.11.0" date="2024-06-05">
   <description/>
  </release>
  <release version="0.10.1" date="2024-04-21"/>
  <release version="0.10.0" date="2024-04-17"/>
  <release version="0.9.1" date="2024-02-26"/>
  <release date="2024-01-27" version="0.9.0">
   <description>
     <p>
       Version 0.9.0 of Supersonic
     </p>

     <p>
       Added
     </p>
     <ul>
       <li>Allow reordering of tracks in the play queue</li>
       <li>Highlight the icon of the current page's navigation button</li>
       <li>Show release type in album page header (for OpenSubsonic servers)</li>
       <li>Setting to save and reload play queue on exit/startup</li>
       <li>Use most recent playlist as default in "Add to playlist" dialog</li>
       <li>Option to show desktop notifications on track change</li>
       <li>Added icons to context menu items</li>
     </ul>

     <p>
       Fixed
     </p>
     <ul>
       <li>OpenGL startup error on some hardware</li>
     </ul>

   </description>
  </release>
 </releases>
</component>
EOF

%build
%set_build_flags

export CGO_ENABLED=1

go build -v -mod=mod -trimpath -buildmode=pie -ldflags="-s -w" -o %{name} .

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

cp res/supersonic-desktop.desktop res/%{app_id}.desktop
mkdir -p %{buildroot}%{_datadir}/applications

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

mkdir -p %{buildroot}%{_metainfodir}
install -Dm644 %{app_id}.metainfo.xml %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.22.0-1
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

* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 0.21.1-1
- Initial release.
