import axios from "axios";

export default class BookingClient {
  constructor(domain, config = null) {
    this.domain = domain;
    this.config = config;
  }

  formatUri(uri) {
    uri = uri.toLocaleLowerCase();
    if (uri.charAt(0) != "/") uri = "/" + uri;
    if (uri.charAt(uri.length - 1) != "/") uri += "/";
    return uri;
  }

  async postAsync(uri, data) {
    uri = this.formatUri(uri);
    const res = await axios.post(this.domain + uri, data, this.config);
    console.log(res.data);
    return res.data;
  }

  async getAsync(uri, params) {
    uri = this.formatUri(uri);
    const res = await axios.get(this.domain + uri, this.config, { params });
    console.log(res.data);
    return res.data;
  }
}
