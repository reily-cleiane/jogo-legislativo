import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

export interface AcaoDia {
  nome: string;
  //efeitos: Partial<GameState>;
}

export interface GameState {
  dia: number;
  tem_reuniao: number;
  em_reuniao: number;
  faltas: number;

  desempenho: number;
  transparencia: number;
  informacao: number;
  crise: number;
  popularidade: number;

  orcamento_aprovado: number;
  verba: number;

  acoes_dia: AcaoDia[];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  constructor(private http: HttpClient) {
    this.pegarEstadosIniciais();
  }
  title = 'app';

  acoes = [
    {nome: 'entrar_reuniao', descricao: 'Entrar em reunião'},
    {nome: 'sair_reuniao', descricao: 'Sair de reunião'},
    {nome: 'justificar_ausencia', descricao: 'Justificar ausência'},
    {nome: 'elaborar_pl', descricao: 'Elaborar projeto de lei'},
    {nome: 'relatar_pl', descricao: 'Relatar projeto de lei'},
    {nome: 'divulgar_gastos', descricao: 'Divulgar gastos do gabinete'},
    {nome: 'acessar_diario', descricao: 'Ler diário oficial'},
    {nome: 'votar_materia', descricao: 'Votar matéria'},
    {nome: 'discutir_materia', descricao: 'Discutir matéria'},
    {nome: 'atender_populacao', descricao: 'Atender população'},
    {nome: 'convocar_audiencia', descricao: 'Convocar audiência pública'},
    {nome: 'aprovar_orcamento', descricao: 'Aprovar orçamento'},
    {nome: 'tarefas_admin', descricao: 'Realizar tarefa administrativas'},
    {nome: 'lidar_crise', descricao: 'Resolver crise'},
    {nome: 'acao_social', descricao: 'Realizar ação social'},

  ]

  estadoInicial: GameState = {
    dia: 1,
    tem_reuniao: 1,
    em_reuniao: 0,
    faltas: 0,

    desempenho: 0,
    transparencia: 10,
    informacao: 10,
    crise: 0,
    popularidade: 10,

    orcamento_aprovado: 0,
    verba: 60000,

    acoes_dia: []
  };

  estadoJogador: GameState = structuredClone(this.estadoInicial);
  estadoAgente: GameState   = structuredClone(this.estadoInicial);
  acoesAgenteExecutadas: any[] = [];
  filaExecucaoAgente: {
    acao: string;
    estado: any;
  }[] = [];

  logAgente: any[] = [];

  pegarEstadosIniciais() {
    this.http.get<any>('http://localhost:8000/inicio')
      .subscribe(res => {

        this.estadoJogador = res.estadoJogador;

        // estado inicial do agente (antes das ações)
        this.estadoAgente = structuredClone(res.estadoJogador);

        this.prepararExecucaoAgente(
          res.acoesAgente,
          res.estadosResultantes,
          res.estadoViradaDia
        );
      });
  }

  prepararExecucaoAgente(
    acoes: string[],
    estados: any[],
    estadoViradaDia: any
  ) {
    this.acoesAgenteExecutadas = [];

    this.filaExecucaoAgente = acoes.map((acao, i) => ({
      acao,
      estado: estados[i]
    }));

    this.executarFilaAgente(estadoViradaDia);
  }

  executarFilaAgente(estadoViradaDia: any) {
    const delay = 5000;

    this.filaExecucaoAgente.forEach((item, index) => {
      setTimeout(() => {

        // atualiza estado visível
        this.estadoAgente = structuredClone(item.estado);

        // adiciona ação ao histórico visual
        this.acoesAgenteExecutadas.push({
          nome: item.acao
        });

        // se for a última ação → virada do dia
        if (index === this.filaExecucaoAgente.length - 1) {
          setTimeout(() => {
            this.estadoAgente = structuredClone(estadoViradaDia);
          }, delay);
        }

      }, delay * index);
    });
  }

  executarAcao(acao: string) {
    this.http.post<any>('http://localhost:8000/acao', { acao })
      .subscribe(res => {

        this.estadoJogador = res.estadoJogador;

        if (res.virouDia) {
          this.prepararExecucaoAgente(
            res.acoesAgente,
            res.estadosResultantes,
            res.estadoViradaDia
          );
        }
      });
  }

}