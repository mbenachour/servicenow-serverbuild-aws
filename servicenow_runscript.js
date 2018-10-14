var os = current.variables.os;
var inst_size = current.variables.inst_size;

var request = new sn_ws.RESTMessageV2();
request.setEndpoint('https://9drnhpoorj.execute-api.us-east-1.amazonaws.com/dev/instance');
request.setBasicAuth("apikey1", "mutKJWAolp3BJZvChmbYm3mHLGrqrPZeaLNFQQvq");
request.setHttpMethod('POST');
request.setRequestHeader("Accept", "application/json");
request.setStringParameterNoEscape('os', current.variables.os);
request.setStringParameterNoEscape('inst_size', current.variables.inst_size);
request.setStringParameterNoEscape('volume_size', current.variables.volume_size1);
request.setRequestHeader('Content-Type', 'application/json');
request.setRequestBody('{"os":"${os}","inst_size":"${inst_size}"}');
var response = request.execute();
gs.log("ec2_server_build" + response.getBody());