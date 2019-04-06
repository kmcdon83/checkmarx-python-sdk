import CxService

cx_config = {
    "preset": "Checkmarx Default",
    "configuration": "Default Configuration",
    "team": "\CxServer\SP\Checkmarx",
    "project": "Lambda",
    "file": "riches.net.zip"
}

cx = CxService.CxService("http://checkmarx.local/CxRestAPI", "admin", "xxxxxx", cx_config)
cx.start_scan(cx_config)
