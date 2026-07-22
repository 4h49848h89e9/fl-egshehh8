
#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <windows.h>

using namespace flutter;

class VpnPlugin {
public:
    static void RegisterWithRegistrar(PluginRegistrarWindows* registrar) {
        auto channel = std::make_unique<MethodChannel<>>(
            registrar->messenger(), "com.oryvexvpn/vpn",
            &StandardMethodCodec::GetInstance());
        auto* channel_raw = channel.get();
        registrar->AddPlugin(std::move(channel));
        channel_raw->SetMethodCallHandler([](const MethodCall<>& call,
                                             std::unique_ptr<MethodResult<>> result) {
            if (call.method_name() == "connect") {
                // TODO: Start Xray/Aether processes
                result->Success();
            } else if (call.method_name() == "disconnect") {
                // TODO: Stop processes
                result->Success();
            } else if (call.method_name() == "getTrafficStats") {
                auto map = std::make_unique<flutter::EncodableMap>();
                (*map)[flutter::EncodableValue("ping")] = flutter::EncodableValue("42 ms");
                (*map)[flutter::EncodableValue("downloadSpeed")] = flutter::EncodableValue("0 B/s");
                (*map)[flutter::EncodableValue("uploadSpeed")] = flutter::EncodableValue("0 B/s");
                (*map)[flutter::EncodableValue("downloadTotal")] = flutter::EncodableValue("0 B");
                (*map)[flutter::EncodableValue("uploadTotal")] = flutter::EncodableValue("0 B");
                result->Success(flutter::EncodableValue(std::move(map)));
            } else if (call.method_name() == "getConfig") {
                result->Success(flutter::EncodableValue("{\\"status\\":\\"ok\\"}"));
            } else if (call.method_name() == "saveConfig") {
                result->Success();
            } else if (call.method_name() == "uninstallCertificate") {
                result->Success();
            } else if (call.method_name() == "clearLogs") {
                result->Success();
            } else if (call.method_name() == "runDiagnostics") {
                result->Success(flutter::EncodableValue("Diagnostics OK"));
            } else {
                result->NotImplemented();
            }
        });
    }
};

extern "C" __declspec(dllexport) void RegisterPlugins(
    PluginRegistrarWindows* registrar) {
    VpnPlugin::RegisterWithRegistrar(registrar);
}
