+++ TRABALHO PRÁTICO DE REDES I +++

	Este trabalho prático propõe a criação de uma topologia de rede virtual a fim de testar e analisar seu comportamento de acordo com situações hipotéticas e de aplicação real. Empregou-se o uso de uma máquina virtual (mininet) que realiza simulações de topologias de rede por meio de códigos de programação na linguagem Python. 

	A criação da topologia de rede, tencionou-se em um código, tendo como principal aspecto a não limitação por quantidade de hosts ou switches. O objetivo foi que este fosse o mais genérico possível, capaz de gerar de forma prática e eficiente, dado uma política, uma topologia para n hosts (único parâmetro a ser passado), levando em consideração que a topologia aceita switches de até 24 portas. A política definida preceitua que, dado n hosts, se n for menor ou igual a capacidade máxima de um switch, estes serão dispostos em um único switch. Caso n seja maior que a capacidade, serão adicionados quantos switches  forem necessários, considerando que a disposição dos hosts nestes será da forma mais igualitária possível, isto é, cada switch terá uma quantidade igual de hosts. Se a divisão do número de hosts pelo de switches resultar em um número inteiro, isto significa que cada switch terá uma quantidade igual de hosts a eles dispostos. Já na ocorrência da divisão resultar em um número real, todos os switches terão quantidades iguais de hosts, exceto pelo último, que terá a mesma quantidade mais o restante. Após isto, o vetor de switches será interconectado bidirecionalmente em série, seguindo a ordem de criação. 

	Os testes e análises realizados na topologia foram de: geração e criação, isto é, se a divisão e quantidade de switches estavam realmente seguindo a política definida; conectividade, se os hosts e switches estavam sendo corretamente dispostos entre si e se todos os hosts conseguiam "conversar" com todos os demais; definido um tamanho para a janela TCP, análise da capacidade de transferência de dados entre dois hosts (servidor e cliente) por vez; transferência entre dois hosts, dispostos em mesmo switch e em switches diferentes; análise do envio de pacotes em tempo default (10s) entre um servidor e um cliente (1 a 1) e um servidor e 3 clientes (1 para 3); comparação do comportamento da rede nos protocolos TCP e UDP em topologias de aplicação real e hipotéticas.

+++ TESTES E ANÁLISES +++

	1. TERMINAL
		1.2. Assuming that the switche have 24 ports (connectivity_test).
			1.2.1. *1 host will create an one switch.
			1.2.2. *24 hosts will create an one switch.
			1.2.3. *25 hosts will create a two switches.
			1.2.4. *49 hosts will create a three switches and so on.

	2. XTERM
		2.1. Checking the data transfer quantity with setting the TCP window size (50 hosts).
			2.1.1. Considering the default time set in 10 sec, in default (max size) the data transfer quantity will be more than the TCP window size set in 8000.
			*Client host:
				iperf -c 10.0.0.50 -p 5566
				iperf -c 10.0.0.50 -p 5566 -w 8000

			*Server host:
				iperf -s -i 1 -p 5566

		2.2. Checking the the data transfer speed between two host (same switch and different switches).
			2.2.1. If the switches connection is a serial interconnection, hosts on same switch, in 10 sec (default), can to send more data than hosts in different switches.
				*Client host:
					iperf -c 10.0.0.2 -p 5566
					iperf -c 10.0.0.50 -p 5566

				*Server host:
					iperf -s -i 1 -p 5566

			2.2.2 One server connected with three clients in default time will get less data transfer quantity than one to one.
				*Client host:
					iperf -c 10.0.0.1 -p 5566
					iperf -c 10.0.0.1 -p 5566
					iperf -c 10.0.0.1 -p 5566

				*Server host:
					iperf -s -i 1 -p 5566

		2.3. Checking data traffic with other parameters (50 hosts, TCP protocol)
			2.3.1. default_topology_generator.py
				sudo python default_topology_generator.py 50

				*Client host:
					iperf -c 10.0.0.50 -t 25 -p 5566

				*Server host:
					iperf -s -i 1 -p 5566 > tcpA
					cat tcpA | grep sec | head -n 25 | tr - " " | awk '{print $3,$7}' > my_tcpA

			2.3.2. topology_parameter_generator.py (Band width = 7Mbps, Delay = 3ms, Loss = 0%, Max queue size = 800)
				sudo python topology_parameter_generator.py 50

				*Client host:
					iperf -c 10.0.0.50 -t 25 -p 5566

				*Server host:
					iperf -s -i 1 -p 5566 > tcpB
					cat tcpB | grep sec | head -n 25 | tr - " " | awk '{print $3,$7}' > my_tcpB

			2.3.3. GnuPlot:
				gnuplot
					set title "Perfect network topology x Network topology in real application (TCP protocol)"
					set xlabel "Time (sec)"
					set ylabel "Throughput (Mbps)"
					set xrange [0:25]
					set xtics 0,1,25
					set yrange [0:10]
					set ytics 0,1,10
					plot "my_tcpA" title "Max use of network parameters" with linespoints, "my_tcpB" title "Real use application" with linespoints

		2.4. Checking data traffic with other parameters (50 hosts, UDP protocol)
			2.4.1. default_topology_generator.py
				sudo python default_topology_generator.py 50

				*Client host:
					iperf -c 10.0.0.50 -t 25 -p 5566 -u -b 7M

				*Server host:
					iperf -s -i 1 -p 5566 -u > udpA
					cat udpA | grep sec | head -n 25 | tr - " " | awk '{print $3,$7}' > my_udpA

			2.4.2. topology_parameter_generator.py (Band width = 5Mbps, Delay = 3ms, Loss = 0%, Max queue size = 800)
				sudo python topology_parameter_generator.py 50

				*Client host:
					iperf -c 10.0.0.50 -t 25 -p 5566 -u -b 7M

				*Server host:
					iperf -s -i 1 -p 5566 -u > udpB
					cat udpB | grep sec | head -n 25 | tr - " " | awk '{print $3,$7}' > my_udpB

			2.4.3. GnuPlot:
				gnuplot
					set title "Perfect network topology x Network topology in real application (UDP protocol)"
					set xlabel "Time (sec)"
					set ylabel "Throughput (Mbps)"
					set xrange [0:20]
					set xtics 0,1,20
					set yrange [0:10]
					set ytics 0,1,10
					plot "my_udpA" title "Max use of network parameters" with linespoints, "my_udpB" title "Real use application" with linespoints

					plot "my_tcpA" title "Max use of network parameters (TCP)" with linespoints, "my_tcpB" title "Real use application (TCP)" with linespoints, "my_udpA" title "Max use of network parameters(UDP)" with linespoints, "my_udpB" title "Real use application (UDP)" with linespoints
