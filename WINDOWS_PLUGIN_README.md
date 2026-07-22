
# Native VPN Plugin Integration

The plugin is already generated in `windows/plugins/vpn_plugin/`.

## For the build to work, you must:

1. **Run `flutter create --platforms=windows .`** if you haven't already. This creates the base Windows runner.

2. **Modify `windows/runner/CMakeLists.txt`** to include the plugin:
   - Add `add_subdirectory(../plugins/vpn_plugin vpn_plugin)` after the `flutter` subdirectory inclusion.
   - Add `target_link_libraries(${PROJECT_NAME} PRIVATE vpn_plugin)`.

3. **The GitHub Actions workflow already runs `flutter create`**, so you can commit everything and let it build.

Alternatively, you can run `flutter create .` locally and manually copy the plugin integration steps.

## Full plugin implementation:
- Manages Xray process (start/stop)
- Installs/removes Root CA certificate
- Sets/restores Windows system proxy
- Provides traffic stats and diagnostics
