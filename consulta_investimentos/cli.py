import click
import pandas as pd

from consulta_investimentos.ativos_cotacoes.cotacoes import consulta_cotacoes
from consulta_investimentos.ativos_posicao.posicao import consulta_posicao
from consulta_investimentos.moeda_cotacao.moedas import consulta_moedas


@click.group('cli')
def cli():
    ...

@cli.command()
@click.argument('empresas', type=click.STRING, nargs=-1, required=True)
@click.option('-dt1', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-dt2', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-e', '--exp', is_flag=True, default=False)
def cotacoes(empresas, dt1, dt2, exp):
    # click.echo('ok')
    dados = consulta_cotacoes(empresas, dt1, dt2)
    if exp is True:
        with pd.ExcelWriter('cotação.xlsx') as writer:
            dados.to_excel(writer, index=False, float_format='%.2f')


@cli.command()
@click.argument('empresas', type=click.STRING, nargs=-1, required=True)
@click.option('-dt1', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-dt2', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-e', '--exp', is_flag=True, default=False)
def dividendos(empresas, dt1, dt2, exp):
    dados = consulta_dividendos(empresas, dt1, dt2)
    if exp is True:
        with pd.ExcelWriter('dividendos.xlsx') as writer:
            dados.to_excel(writer, index=False, float_format='%.2f')


@cli.command()
@click.argument('empresas', type=click.STRING, nargs=-1, required=True)
@click.option('-dt1', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-dt2', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-e', '--exp', is_flag=True, default=False)
def eventos(empresas, dt1, dt2, exp):
    dados = consulta_eventos(empresas, dt1, dt2)
    if exp is True:
        with pd.ExcelWriter('eventos.xlsx') as writer:
            dados.to_excel(writer, index=False, float_format='%.2f')


@cli.command()
@click.argument('path_download', type=click.Path(exists=True), required=True)
@click.option('-dt1', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-dt2', type=click.DateTime(formats=['%d/%m/%Y']), required=True)
@click.option('-e', '--exp', is_flag=True, default=False)
def posicao(path_download, dt1, dt2, exp):
    dados = consulta_posicao(path_download, dt1, dt2)
    if exp is True:
        with pd.ExcelWriter('posicao.xlsx') as writer:
            dados.to_excel(writer, index=False, float_format='%.2f')

@cli.command()
@click.argument('moeda_base', type=click.STRING, required=True)
@click.argument('moeda_destino', type=click.STRING, required=True)
@click.option('-v', '--valor', type=click.STRING, default=1, required=False)
@click.option('-dt1', type=click.DateTime(formats=['%d/%m/%Y']), default=None, required=False)
@click.option('-dt2', type=click.DateTime(formats=['%d/%m/%Y']), default=None, required=False)
@click.option('-e', '--exp', is_flag=True, default=False)
def moeda(moeda_base, moeda_destino, valor, dt1, dt2, exp):
    dados = consulta_moedas(moeda_base, moeda_destino, valor, dt1, dt2)
    if exp is True:
        with pd.ExcelWriter('moedas.xlsx') as writer:
            dados.to_excel(writer, index=False, float_format='%.2f')
