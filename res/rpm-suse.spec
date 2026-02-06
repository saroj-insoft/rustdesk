Name:       ez2desk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/ez2desk/
mkdir -p %{buildroot}/usr/share/ez2desk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/rustdesk %{buildroot}/usr/bin/ez2desk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/ez2desk/libsciter-gtk.so
install $HBB/res/ez2desk.service %{buildroot}/usr/share/ez2desk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/rustdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/rustdesk.svg
install $HBB/res/rustdesk.desktop %{buildroot}/usr/share/ez2desk/files/
install $HBB/res/rustdesk-link.desktop %{buildroot}/usr/share/ez2desk/files/

%files
/usr/bin/ez2desk
/usr/share/ez2desk/libsciter-gtk.so
/usr/share/ez2desk/files/ez2desk.service
/usr/share/icons/hicolor/256x256/apps/rustdesk.png
/usr/share/icons/hicolor/scalable/apps/rustdesk.svg
/usr/share/ez2desk/files/rustdesk.desktop
/usr/share/ez2desk/files/rustdesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop ez2desk || true
    systemctl stop rustdesk || true
  ;;
esac

%post
cp /usr/share/ez2desk/files/ez2desk.service /etc/systemd/system/ez2desk.service
rm -f /etc/systemd/system/rustdesk.service || true
cp /usr/share/ez2desk/files/rustdesk.desktop /usr/share/applications/
cp /usr/share/ez2desk/files/rustdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable ez2desk
systemctl start ez2desk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop ez2desk || true
    systemctl disable ez2desk || true
    systemctl stop rustdesk || true
    systemctl disable rustdesk || true
    rm /etc/systemd/system/ez2desk.service || true
    rm /etc/systemd/system/rustdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/rustdesk.desktop || true
    rm /usr/share/applications/rustdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
