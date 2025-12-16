import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
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

  executarAcao(nome:string){
    console.log("acao", nome)
  }
}
