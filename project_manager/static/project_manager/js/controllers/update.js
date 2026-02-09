window.onload = function(){
    console.log('update')
    let originalPath = window.location.pathname;
    if (originalPath.startsWith("/")) {
        originalPath = originalPath.slice(1);
    }
    if (originalPath.endsWith("/")) {
        originalPath = originalPath.slice(0, -1);
    }
    const pathStrSplit = originalPath.split("/");
    pathStrSplit.pop();
    let urlPath;
    const successUrlPath = "/" + pathStrSplit.join("/") + "/";
    console.log(pathStrSplit);
    if (pathStrSplit[2] === "sub-plugins") {
        urlPath = "/api/sub-plugins/releases/" + pathStrSplit[1] + "/" + pathStrSplit[3] + "/";
    } else {
        urlPath = "/api/" + pathStrSplit[0] + "/releases/" + pathStrSplit[1] + "/"
    }
    console.log(urlPath);
    console.log(successUrlPath);
};
