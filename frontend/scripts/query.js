const params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});

const { endpoint, domain, index } = params;

var changed = 0;

if (endpoint !== undefined) {
  document.getElementById("endpoint").value += endpoint;
  changed++;
}

if (domain !== undefined) {
  document.getElementById("domain").value += domain;
  changed++;
}

if (index !== undefined) {
  document.getElementById("index").value += index;
  changed++;
}

if( changed == 3) {
  // Run query
}