
#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <windows.h>
#include <wininet.h>
#include <winreg.h>
#include <wincrypt.h>
#include <tlhelp32.h>
#include <shlwapi.h>
#include <psapi.h>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <filesystem>
#include <chrono>

#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "crypt32.lib")
#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "psapi.lib")

using namespace flutter;

namespace fs = std::filesystem;

// --------------------------------------------------------------
//  Helper functions
// --------------------------------------------------------------
std::wstring ToWString(const std::string& s) {
    int len = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, NULL, 0);
    std::wstring wstr(len, 0);
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, &wstr[0], len);
    return wstr;
}

std::string ToString(const std::wstring& wstr) {
    int len = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, NULL, 0, NULL, NULL);
    std::string str(len, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, &str[0], len, NULL, NULL);
    return str;
}

std::wstring GetAppDir() {
    wchar_t path[MAX_PATH];
    GetModuleFileNameW(NULL, path, MAX_PATH);
    fs::path exe(path);
    return exe.parent_path().wstring();
}

std::wstring GetCoreDir() {
    return GetAppDir() + L"\\assets\\core";
}

std::wstring GetConfigPath() {
    return GetAppDir() + L"\\assets\\config\\oryvexvpn-config.json";
}

// --------------------------------------------------------------
//  Certificate installation (Current User Root)
// --------------------------------------------------------------
bool InstallCertificate(const std::wstring& certPath) {
    HCERTSTORE hStore = CertOpenStore(CERT_STORE_PROV_SYSTEM_W, 0, NULL,
                                       CERT_SYSTEM_STORE_CURRENT_USER, L"Root");
    if (!hStore) return false;
    bool ok = false;
    HANDLE hFile = CreateFileW(certPath.c_str(), GENERIC_READ, FILE_SHARE_READ,
                               NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        DWORD size = GetFileSize(hFile, NULL);
        if (size > 0) {
            std::vector<BYTE> buf(size);
            DWORD read;
            if (ReadFile(hFile, buf.data(), size, &read, NULL) && read == size) {
                PCCERT_CONTEXT pCert = CertCreateCertificateContext(X509_ASN_ENCODING, buf.data(), size);
                if (pCert) {
                    if (CertAddCertificateContextToStore(hStore, pCert, CERT_STORE_ADD_ALWAYS, NULL)) {
                        ok = true;
                    }
                    CertFreeCertificateContext(pCert);
                }
            }
        }
        CloseHandle(hFile);
    }
    CertCloseStore(hStore, 0);
    return ok;
}

bool UninstallCertificate(const std::wstring& certPath) {
    HCERTSTORE hStore = CertOpenStore(CERT_STORE_PROV_SYSTEM_W, 0, NULL,
                                       CERT_SYSTEM_STORE_CURRENT_USER, L"Root");
    if (!hStore) return false;
    bool ok = false;
    HANDLE hFile = CreateFileW(certPath.c_str(), GENERIC_READ, FILE_SHARE_READ,
                               NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        DWORD size = GetFileSize(hFile, NULL);
        if (size > 0) {
            std::vector<BYTE> buf(size);
            DWORD read;
            if (ReadFile(hFile, buf.data(), size, &read, NULL) && read == size) {
                PCCERT_CONTEXT pCert = CertCreateCertificateContext(X509_ASN_ENCODING, buf.data(), size);
                if (pCert) {
                    PCCERT_CONTEXT pFound = CertFindCertificateInStore(hStore, X509_ASN_ENCODING, 0,
                                                                        CERT_FIND_EXISTING, pCert, NULL);
                    if (pFound) {
                        if (CertDeleteCertificateFromStore(pFound)) ok = true;
                        CertFreeCertificateContext(pFound);
                    }
                    CertFreeCertificateContext(pCert);
                }
            }
        }
        CloseHandle(hFile);
    }
    CertCloseStore(hStore, 0);
    return ok;
}

bool IsCertificateInstalled(const std::wstring& certPath) {
    HCERTSTORE hStore = CertOpenStore(CERT_STORE_PROV_SYSTEM_W, 0, NULL,
                                       CERT_SYSTEM_STORE_CURRENT_USER, L"Root");
    if (!hStore) return false;
    bool found = false;
    HANDLE hFile = CreateFileW(certPath.c_str(), GENERIC_READ, FILE_SHARE_READ,
                               NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        DWORD size = GetFileSize(hFile, NULL);
        if (size > 0) {
            std::vector<BYTE> buf(size);
            DWORD read;
            if (ReadFile(hFile, buf.data(), size, &read, NULL) && read == size) {
                PCCERT_CONTEXT pCert = CertCreateCertificateContext(X509_ASN_ENCODING, buf.data(), size);
                if (pCert) {
                    PCCERT_CONTEXT pFound = CertFindCertificateInStore(hStore, X509_ASN_ENCODING, 0,
                                                                        CERT_FIND_EXISTING, pCert, NULL);
                    if (pFound) {
                        found = true;
                        CertFreeCertificateContext(pFound);
                    }
                    CertFreeCertificateContext(pCert);
                }
            }
        }
        CloseHandle(hFile);
    }
    CertCloseStore(hStore, 0);
    return found;
}

// --------------------------------------------------------------
//  Generate certificate using xray.exe
// --------------------------------------------------------------
bool GenerateCertificate(const std::wstring& coreDir) {
    std::wstring xrayPath = coreDir + L"\\xray.exe";
    if (!fs::exists(xrayPath)) return false;
    std::wstring cmd = L"\"" + xrayPath + L"\" tls cert -ca -file=mycert";
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    if (!CreateProcessW(NULL, &cmd[0], NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL,
                         coreDir.c_str(), &si, &pi)) {
        return false;
    }
    WaitForSingleObject(pi.hProcess, 15000);
    DWORD exitCode;
    GetExitCodeProcess(pi.hProcess, &exitCode);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return exitCode == 0;
}

// --------------------------------------------------------------
//  Process management
// --------------------------------------------------------------
DWORD FindProcessByName(const std::wstring& name) {
    DWORD pid = 0;
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snap != INVALID_HANDLE_VALUE) {
        PROCESSENTRY32W pe;
        pe.dwSize = sizeof(pe);
        if (Process32FirstW(snap, &pe)) {
            do {
                if (_wcsicmp(pe.szExeFile, name.c_str()) == 0) {
                    pid = pe.th32ProcessID;
                    break;
                }
            } while (Process32NextW(snap, &pe));
        }
        CloseHandle(snap);
    }
    return pid;
}

void KillProcess(const std::wstring& name) {
    DWORD pid = FindProcessByName(name);
    if (pid) {
        HANDLE h = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
        if (h) {
            TerminateProcess(h, 0);
            WaitForSingleObject(h, 3000);
            CloseHandle(h);
        }
    }
}

// --------------------------------------------------------------
//  System proxy (registry)
// --------------------------------------------------------------
const wchar_t* INTERNET_SETTINGS = L"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings";

void SetSystemProxy(bool enable, int port) {
    HKEY hKey;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, INTERNET_SETTINGS, 0, KEY_SET_VALUE, &hKey) != ERROR_SUCCESS) return;
    DWORD proxyEnable = enable ? 1 : 0;
    RegSetValueExW(hKey, L"ProxyEnable", 0, REG_DWORD, (BYTE*)&proxyEnable, sizeof(DWORD));
    if (enable) {
        std::wstring proxy = L"http=127.0.0.1:" + std::to_wstring(port) + L";https=127.0.0.1:" + std::to_wstring(port);
        RegSetValueExW(hKey, L"ProxyServer", 0, REG_SZ, (BYTE*)proxy.c_str(), (DWORD)((proxy.size()+1)*sizeof(wchar_t)));
        RegSetValueExW(hKey, L"ProxyOverride", 0, REG_SZ, (BYTE*)L"<local>;127.0.0.1;localhost", 0);
    } else {
        RegDeleteValueW(hKey, L"ProxyServer");
        RegDeleteValueW(hKey, L"ProxyOverride");
    }
    RegCloseKey(hKey);
    // Notify changes
    InternetSetOptionW(NULL, INTERNET_OPTION_SETTINGS_CHANGED, NULL, 0);
    InternetSetOptionW(NULL, INTERNET_OPTION_REFRESH, NULL, 0);
}

// --------------------------------------------------------------
//  Xray core start/stop
// --------------------------------------------------------------
DWORD g_xrayPid = 0;

bool StartXray(const std::wstring& coreDir, const std::wstring& configPath, int port) {
    // Kill any existing
    KillProcess(L"xray.exe");
    g_xrayPid = 0;

    std::wstring xrayPath = coreDir + L"\\xray.exe";
    if (!fs::exists(xrayPath)) return false;
    std::wstring cmd = L"\"" + xrayPath + L"\" run -c \"" + configPath + L"\"";
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    if (!CreateProcessW(NULL, &cmd[0], NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL,
                         coreDir.c_str(), &si, &pi)) {
        return false;
    }
    g_xrayPid = pi.dwProcessId;
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return true;
}

void StopXray() {
    KillProcess(L"xray.exe");
    g_xrayPid = 0;
}

// --------------------------------------------------------------
//  Traffic stats (using GetIfTable)
// --------------------------------------------------------------
#include <iphlpapi.h>
#pragma comment(lib, "iphlpapi.lib")

std::string FormatSize(long long bytes) {
    if (bytes >= 1073741824) return std::to_string(bytes / 1073741824) + " GB";
    if (bytes >= 1048576) return std::to_string(bytes / 1048576) + " MB";
    if (bytes >= 1024) return std::to_string(bytes / 1024) + " KB";
    return std::to_string(bytes) + " B";
}

struct TrafficStats {
    long long dlSpeed = 0;
    long long ulSpeed = 0;
    long long dlTotal = 0;
    long long ulTotal = 0;
    std::string ping = "-- ms";
};

TrafficStats GetTrafficStats() {
    static long long prevDl = 0, prevUl = 0;
    static auto lastTime = std::chrono::steady_clock::now();

    TrafficStats stats;
    MIB_IFTABLE* pTable = NULL;
    DWORD size = 0;
    if (GetIfTable(NULL, &size, FALSE) == ERROR_INSUFFICIENT_BUFFER) {
        pTable = (MIB_IFTABLE*)malloc(size);
        if (pTable && GetIfTable(pTable, &size, FALSE) == NO_ERROR) {
            for (DWORD i = 0; i < pTable->dwNumEntries; i++) {
                if (pTable->table[i].dwOperStatus == IF_OPER_STATUS_UP &&
                    pTable->table[i].dwType != IF_TYPE_SOFTWARE_LOOPBACK) {
                    stats.dlTotal += pTable->table[i].dwInOctets;
                    stats.ulTotal += pTable->table[i].dwOutOctets;
                }
            }
        }
        free(pTable);
    }
    // Calculate speed
    auto now = std::chrono::steady_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::milliseconds>(now - lastTime).count();
    if (diff > 0) {
        stats.dlSpeed = (stats.dlTotal - prevDl) * 1000 / diff;
        stats.ulSpeed = (stats.ulTotal - prevUl) * 1000 / diff;
    }
    prevDl = stats.dlTotal;
    prevUl = stats.ulTotal;
    lastTime = now;

    // Ping (mock)
    stats.ping = "42 ms";
    return stats;
}

// --------------------------------------------------------------
//  Plugin class
// --------------------------------------------------------------
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
                // Extract port (optional)
                int port = 10808;
                std::wstring coreDir = GetCoreDir();
                std::wstring configPath = GetConfigPath();
                std::wstring certPath = coreDir + L"\\mycert.crt";
                std::wstring keyPath = coreDir + L"\\mycert.key";

                // Generate cert if missing
                if (!fs::exists(certPath) || !fs::exists(keyPath)) {
                    if (!GenerateCertificate(coreDir)) {
                        result->Error("CERT_FAIL", "Failed to generate certificate");
                        return;
                    }
                }
                // Install cert
                if (!IsCertificateInstalled(certPath)) {
                    if (!InstallCertificate(certPath)) {
                        result->Error("CERT_INSTALL_FAIL", "Could not install certificate");
                        return;
                    }
                }
                // Start xray
                if (!StartXray(coreDir, configPath, port)) {
                    result->Error("XRAY_FAIL", "Failed to start xray.exe");
                    return;
                }
                // Set system proxy
                SetSystemProxy(true, port);
                result->Success();
            } else if (call.method_name() == "disconnect") {
                StopXray();
                SetSystemProxy(false, 0);
                result->Success();
            } else if (call.method_name() == "getTrafficStats") {
                auto stats = GetTrafficStats();
                auto map = std::make_unique<flutter::EncodableMap>();
                (*map)[flutter::EncodableValue("ping")] = flutter::EncodableValue(stats.ping);
                (*map)[flutter::EncodableValue("downloadSpeed")] = flutter::EncodableValue(FormatSize(stats.dlSpeed) + "/s");
                (*map)[flutter::EncodableValue("uploadSpeed")] = flutter::EncodableValue(FormatSize(stats.ulSpeed) + "/s");
                (*map)[flutter::EncodableValue("downloadTotal")] = flutter::EncodableValue(FormatSize(stats.dlTotal));
                (*map)[flutter::EncodableValue("uploadTotal")] = flutter::EncodableValue(FormatSize(stats.ulTotal));
                result->Success(flutter::EncodableValue(std::move(map)));
            } else if (call.method_name() == "getConfig") {
                std::wstring path = GetConfigPath();
                if (fs::exists(path)) {
                    std::ifstream f(path);
                    std::string content((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
                    result->Success(flutter::EncodableValue(content));
                } else {
                    result->Error("NOT_FOUND", "Config file missing");
                }
            } else if (call.method_name() == "saveConfig") {
                std::string content = std::get<std::string>(*call.arguments());
                std::wstring path = GetConfigPath();
                std::ofstream f(path);
                f << content;
                result->Success();
            } else if (call.method_name() == "uninstallCertificate") {
                std::wstring certPath = GetCoreDir() + L"\\mycert.crt";
                UninstallCertificate(certPath);
                fs::remove(certPath);
                fs::remove(GetCoreDir() + L"\\mycert.key");
                result->Success();
            } else if (call.method_name() == "clearLogs") {
                // Not implemented in native, handled by Dart
                result->Success();
            } else if (call.method_name() == "runDiagnostics") {
                std::stringstream ss;
                ss << "Diagnostics started...\\n";
                ss << "Xray exe: " << (fs::exists(GetCoreDir() + L"\\xray.exe") ? "OK" : "MISSING") << "\\n";
                ss << "Config: " << (fs::exists(GetConfigPath()) ? "OK" : "MISSING") << "\\n";
                ss << "Certificate: " << (IsCertificateInstalled(GetCoreDir() + L"\\mycert.crt") ? "Installed" : "Not installed") << "\\n";
                ss << "Port: " << (FindProcessByName(L"xray.exe") ? "Xray running" : "Xray stopped") << "\\n";
                result->Success(flutter::EncodableValue(ss.str()));
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
