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
            tableBody.innerHTML = ''; // Limpar a tabela antes de popular

            if (data && data.travels && data.travels.length > 0) {
                data.travels.forEach(travel => {
                    console.log("Dados da viagem atual:", travel);

                    // Extrair data e hora de departure
                    const departure = new Date(travel.departure);
                    const departureDate = departure.toLocaleDateString();  // Ex: "05/09/2024"
                    const departureTime = departure.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });  // Ex: "14:00"

                    // Extrair data e hora de arrival
                    const arrival = new Date(travel.arrival);

                    // Calcular a duração da viagem
                    const durationMs = arrival.getTime() - departure.getTime();  // Diferença em milissegundos
                    const durationHours = Math.floor(durationMs / (1000 * 60 * 60));  // Converter para horas
                    const durationMinutes = Math.floor((durationMs % (1000 * 60 * 60)) / (1000 * 60));  // Restante em minutos

                    const duration = `${durationHours}h ${durationMinutes}min`;  // Formatar a duração

                    // Definir valores para a tabela
                    const originCity = travel.origin.address.city || "Cidade de origem não encontrada";
                    const destinationCity = travel.destination.address.city || "Cidade de destino não encontrada";
                    const distance = travel.destination.distance || "Distância não encontrada";

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${originCity}</td>
                        <td>${destinationCity}</td>
                        <td>${departureDate}</td>
                        <td>${departureTime}</td> 
                        <td>${distance}</td>
                        <td>${duration}</td>
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

function get_driver_info(travel_id) {
    // Faz a requisição para obter os detalhes da viagem
    fetch(`/travels/search/${travel_id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar detalhes da viagem');
            }
            return response.json();  // Converte a resposta para JSON
        })
        .then(data => {
            if (data && typeof data.user_id !== 'undefined') {
                const user_id = data.user_id;  // Extrai o user_id
                const renavam = data.renavam;  // Extrai o renavam
                // Faz uma nova requisição para buscar os detalhes do usuário
                return fetch(`/users/${user_id}/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro ao buscar detalhes do usuário');
                        }
                        return response.json();  // Converte a resposta para JSON
                    })
                    .then(userData => {
                        if (userData && userData.name) {
                            const userName = userData.name;  // Extrai o nome do usuário
                            return { userName, user_id, renavam }; // Retorna um objeto com userName e renavam
                        } else {
                            throw new Error('Nome do usuário não encontrado.');
                        }
                    });
            } else {
                throw new Error('Nenhum user_id encontrado para essa viagem.');
            }
        })
        .then(({ userName, user_id, renavam }) => {
            // Faz a requisição para buscar os detalhes do motorista
            return fetch(`/drivers/${user_id}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao buscar detalhes do motorista');
                    }
                    return response.json();  // Converte a resposta para JSON
                })
                .then(driverData => {
                    if (driverData && typeof driverData.rating !== 'undefined') {
                        // Usa toFixed(1) para exibir o rating com uma casa decimal
                        const driverRating = driverData.rating.toFixed(1);  
                        console.log('rating motorista:', driverRating);
                        
                        // Agora faz a requisição para buscar os detalhes do carro usando o renavam
                        return fetch(`/cars/search/${renavam}/`)
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Erro ao buscar detalhes do carro');
                                }
                                return response.json();  // Converte a resposta para JSON
                            })
                            .then(carData => {
                                if (carData && carData.brand && carData.model && carData.plate && carData.color) {
                                    // Monta a linha da tabela com todas as informações
                                    const row = document.createElement('tr');
                                    row.innerHTML = `
                                        <td>${userName}</td>
                                        <td>${carData.brand} ${carData.model} (${carData.color})</td>
                                        <td>${carData.plate}</td>
                                        <td>${driverRating}</td>
                                        <td><a href="/rate/rate-driver/${user_id}" class="button-details">Avaliar</a></td>
                                    `;

                                    // Adiciona a linha na tabela
                                    const tableBody = document.getElementById('travel-table-body');
                                    tableBody.innerHTML = ''; // Limpar a tabela antes de popular
                                    if (tableBody) {
                                        tableBody.appendChild(row);  // Adiciona a linha à tabela
                                    } else {
                                        console.error('Elemento com id "travel-table-body" não encontrado.');
                                    }
                                } else {
                                    throw new Error('Detalhes do carro não encontrados.');
                                }
                            });
                    } else {
                        throw new Error('Avaliação do motorista não encontrada.');
                    }
                });
        })
        .catch(error => {
            console.error('Erro ao buscar informações:', error);
        });
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
