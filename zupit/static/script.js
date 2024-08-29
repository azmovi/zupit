function buscarEndereco(cep, destino) {
    const cepLimpo = cep.replace('-', '');
    
    if (cepLimpo.length === 8) {
        fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById(destino).value = `${data.logradouro}, ${data.bairro}, ${data.localidade} - ${data.uf}`;
                } else {
                    alert('CEP não encontrado!');
                }
            })
            .catch(error => {
                console.error('Erro ao buscar o CEP:', error);
                alert('Erro ao buscar o CEP. Verifique a conexão.');
            });
    } else {
        alert('CEP inválido!');
    }
}

function fetchCars(user_id) {
    fetch(`/cars/${user_id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar a lista de carros');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.cars) {
                const selectCar = document.getElementById('car');
                data.cars.forEach(car => {
                    const option = document.createElement('option');
                    option.value = car.renavam;
                    option.textContent = `${car.brand} ${car.model} - ${car.plate} (${car.color})`;
                    selectCar.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Erro ao carregar carros:', error));
}
