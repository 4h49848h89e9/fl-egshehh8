
# Native Windows Plugin Integration

The VPN functionality requires a native plugin to:
- Spawn xray.exe (or aether.exe)
- Set/clear system proxy via Windows Registry
- Generate and trust Root CA certificate

We have provided a stub plugin in `windows/plugins/vpn_plugin/`.

## To integrate:
1. Copy the plugin folder into your Windows runner after `flutter create`.
2. Add the plugin to the main CMakeLists.txt by including the subdirectory and linking.

The GitHub Actions workflow will run `flutter create`, so you may need to copy these files into the generated `windows/` folder after creation. Consider modifying your workflow to copy these files after the `flutter create` step.

Alternatively, you can generate the full Windows project locally once and commit it (removing the `flutter create` step from the workflow).
