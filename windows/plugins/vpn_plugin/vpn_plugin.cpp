
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
