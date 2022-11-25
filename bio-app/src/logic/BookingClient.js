import axios from "axios";

export default class BookingClient {
  constructor(domain) {
    // to lower case and removes trailing '/'
    domain = domain.toLocaleLowerCase();
    if (domain.charAt(domain.length - 1) != "/") domain.slice(0, -1);

    this.domain = domain;
    this.config = {
      headers: {},
      params: {},
    };
  }

  async authenticate(username, password) {
    const response = await this.postAsync("api-token-auth", {
      username: username,
      password: password,
    });
    const token = response.token;
    this.config.headers.Authorization = `Token ${token}`;
  }

  formatUri(uri) {
    uri = uri.toLocaleLowerCase();
    if (uri.charAt(0) != "/") uri = "/" + uri;
    if (uri.charAt(uri.length - 1) != "/") uri += "/";
    return uri;
  }

  async postAsync(uri, data) {
    uri = this.formatUri(uri);
    let responseData;
    try {
      const res = await axios.post(this.domain + uri, data, this.config);
      responseData = res.data;
    } catch (err) {
      console.log(err);
    }
    return responseData;
  }

  async getAsync(uri, params = null) {
    uri = this.formatUri(uri);

    if (params) {
      this.config.params = params;
    }

    const res = await axios.get(this.domain + uri, this.config);

    if (this.config.params) {
      this.config.params = {};
    }
    return res.data;
  }
}
