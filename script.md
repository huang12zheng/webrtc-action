```sh
cd webrtc-build
git diff --cached > ../clone_depot_tools_use_d1.patch
git diff --cached > ../translation_into_english.patch
git diff --cached > ../container_preparations_advance.patch
git diff --cached > ../build_with_component.patch
```

```sh
git clone https://github.com/shiguredo-webrtc-build/webrtc-build.git
cd webrtc-build
patch -i ../clone_depot_tools_use_d1.patch
```