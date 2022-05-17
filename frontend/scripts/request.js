document.getElementById("button").addEventListener("click", runQuery, false);

function runQuery() {
  const endpoint = document.getElementById("endpoint").value;
  const domain = document.getElementById("domain").value;
  const index = document.getElementById("index").value;

  const request = `http://${endpoint}/?domain=${domain}&similarity=${index}`;

  console.log(request);

  fetch(request)
    .then((data) => {
      return data.json();
    })
    .then((res) => {
      console.log(res);
    });
}
