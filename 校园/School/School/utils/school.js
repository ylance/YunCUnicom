
var publickey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzMQlvzBa/SvRBQDFn9AI8QIc/Z0cunFJd9Mo69p+uW8DU6tOnHXBYm/IfXSzBgORDa/eBgpmx9zDWefvnbryrkS4siQplETCzQP+vy7qldtB0iflZZLtyMO3KinKEB4FMv5A9g6oL0ibtO7Pje5wDqru5YJ/HavHzaQHclYSd3w6jiFGJQ4wa2XBpFLC7f7hNVPiXjelKtP+1/RW1Af9oFQpwKo26J2Q0hMufdMovZ+Ww4gZe855IASrOEGJ//MsPRwqgAO8Lys0qK6xX6B0rgSWG7thdzoFsgou1QPQi3pJr1cQpbkxfkSQ9Vsvp3REFwuA0IDt51ex9BcQtEjrBQIDAQAB";
function Encrypt(str) {
	var pwd = publickey;
	if (str == "")
		return "";
	str = escape(str);
	pwd = escape(pwd);
	if (pwd == null || pwd.length <= 0) {
		return "";
	}
	var prand = "";
	for (var I = 0; I < pwd.length; I++) {
		prand += pwd.charCodeAt(I).toString();
	}
	var sPos = Math.floor(prand.length / 5);
	var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos * 2) + prand.charAt(sPos * 3) + prand.charAt(sPos * 4) + prand.charAt(sPos * 5));
	var incr = Math.ceil(pwd.length / 2);
	var modu = Math.pow(2, 31) - 1;
	if (mult < 2) {
		return "";
	}
	var salt = Math.round(Math.random() * 1000000000) % 100000000;
	prand += salt;
	while (prand.length > 10) {
		prand = (parseInt(prand.substring(0, 10)) + parseInt(prand.substring(10, prand.length))).toString();
	}
	prand = (mult * prand + incr) % modu;
	var enc_chr = "";
	var enc_str = "";
	for (var I = 0; I < str.length; I++) {
		enc_chr = parseInt(str.charCodeAt(I) ^ Math.floor((prand / modu) * 255));
		if (enc_chr < 16) {
			enc_str += "0" + enc_chr.toString(16);
		} else
			enc_str += enc_chr.toString(16);
		prand = (mult * prand + incr) % modu;
	}
	salt = salt.toString(16);
	while (salt.length < 8)
		salt = "0" + salt;
	enc_str += salt;
	return enc_str;
}
function Decrypt(str) {
	var pwd = publickey;
	if (str == "")
		return "";
	pwd = escape(pwd);
	if (str == null || str.length < 8) {
		return "";
	}
	if (pwd == null || pwd.length <= 0) {
		return "";
	}
	var prand = "";
	for (var I = 0; I < pwd.length; I++) {
		prand += pwd.charCodeAt(I).toString();
	}
	var sPos = Math.floor(prand.length / 5);
	var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos * 2) + prand.charAt(sPos * 3) + prand.charAt(sPos * 4) + prand.charAt(sPos * 5));
	var incr = Math.round(pwd.length / 2);
	var modu = Math.pow(2, 31) - 1;
	var salt = parseInt(str.substring(str.length - 8, str.length), 16);
	str = str.substring(0, str.length - 8);
	prand += salt;
	while (prand.length > 10) {
		prand = (parseInt(prand.substring(0, 10)) + parseInt(prand.substring(10, prand.length))).toString();
	}
	prand = (mult * prand + incr) % modu;
	var enc_chr = "";
	var enc_str = "";
	for (var I = 0; I < str.length; I += 2) {
		enc_chr = parseInt(parseInt(str.substring(I, I + 2), 16) ^ Math.floor((prand / modu) * 255));
		enc_str += String.fromCharCode(enc_chr);
		prand = (mult * prand + incr) % modu;
	}
	return unescape(enc_str);
}

function sid() {
	var now = +new Date();
	sid = now + "" + Math.round(((Math.random() * 9) + 1) * 100000);
	return sid;
}