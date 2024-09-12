function find_cep(raw_cep) {
    const cep = raw_cep.replace('-', '');
    
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('street').value = data.logradouro;
                    document.getElementById('district').value = data.bairro;
                    document.getElementById('city').value = data.localidade;
                    document.getElementById('state').value = data.uf;
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

function get_cars(user_id) {
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

function get_travels(user_id) {
    fetch(`/travels/${user_id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar a lista de viagens');
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados recebidos:', data);  // Verifique se os dados estão corretos no console
            const tableBody = document.getElementById('travel-table-body');
            
            if (!tableBody) {
                console.error('Elemento com id "travel-table-body" não encontrado.');
                return;
            }

            tableBody.innerHTML = ''; // Limpar a tabela antes de popular

            if (data && data.travels && data.travels.length > 0) {
                data.travels.forEach(travel => {
                    console.log("Dados da viagem atual:", travel);

                    const originCity = travel.pick_up?.city || "Cidade de origem não encontrada";
                    const destinationCity = travel.pick_off?.city || "Cidade de destino não encontrada";
                    const departureTime = travel.departure_time || "Hora de partida não encontrada";
                    const departureDate = travel.departure_date || "Data de partida não encontrada";

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${originCity}</td>
                        <td>${destinationCity}</td>
                        <td>${departureDate}</td>
                        <td>${departureTime}</td>
                        <td>${travel.distance || "Distância não encontrada"}</td>
                        <td>${travel.duration || "Duração não encontrada"}</td>
                        <td><a href="/trip-participants/${travel.id}" class="button-details">Participantes</a></td>
                    `;
                    console.log("id da viagem:", travel.id);
                    console.log("Linha adicionada à tabela:", row.innerHTML);
                    tableBody.appendChild(row);
                });
            } else {
                console.log("Nenhuma viagem encontrada.");
                tableBody.innerHTML = '<tr><td colspan="7">Nenhuma viagem encontrada.</td></tr>';
            }
        })
        .catch(error => console.error('Erro ao carregar viagens:', error));
}

function save_form(step) {
    const form = document.querySelector('form');
    form.addEventListener('submit', function() {
        const data_form = {};
        Array.from(this.elements).forEach(element => {
            if (element.name){
                data_form[element.name] = element.value;
            }
        });
        sessionStorage.setItem(step, JSON.stringify(data_form));
    });
}
