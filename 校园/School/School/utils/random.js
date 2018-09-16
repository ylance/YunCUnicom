function getRandomParam() {
	var date = new Date();
	return "" + date.getYear() + (date.getMonth() + 1) + date.getDate() + date.getHours() + date.getMinutes() + date.getSeconds() + date.getMilliseconds();
}