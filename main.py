import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

CANAIS_BOTOES = [
    "vocês são retardados?",
    "Boa noite Dejota",
    "Oudri Kanda Larrai",
    "Conselho",
    "Core - Revolution",
]


class PainelMover(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for nome_canal in CANAIS_BOTOES:
            self.add_item(BotaoMover(nome_canal))


class BotaoMover(discord.ui.Button):
    def __init__(self, nome_canal):
        super().__init__(
            label=nome_canal,
            style=discord.ButtonStyle.primary,
            custom_id=f"mover_{nome_canal}"
        )
        self.nome_canal = nome_canal

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not interaction.user.voice:
            return

        origem = interaction.user.voice.channel
        destino = discord.utils.get(interaction.guild.voice_channels, name=self.nome_canal)
        cargo = discord.utils.get(interaction.guild.roles, name="Warlord")

        if not destino or not cargo:
            return

        membros = [m for m in origem.members if cargo in m.roles and not m.bot]
        if membros:
            await asyncio.gather(*[m.move_to(destino) for m in membros])


async def setup_hook():
    bot.add_view(PainelMover())

bot.setup_hook = setup_hook


@bot.command()
async def painel(ctx):
    await ctx.message.delete()
    await ctx.send("# Mover Warlords", view=PainelMover())


@bot.command()
async def ajuda(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("🤖 Qual bot você precisa de ajuda?\n- jeeves\n- raidbots\n\nDigite o nome do bot:")

    try:
        resposta = await bot.wait_for('message', check=check, timeout=60.0)
    except:
        await ctx.send("⏱️ Tempo esgotado para responder.")
        return

    escolha = resposta.content.lower().strip()

    if escolha == "raidbots":
        await ctx.send(
            "**📘 Guia de uso do RaidBots:**\n\n"
            "🛠️ Para começar, use o comando `/sim`\n"
            "1. Clique na opção `INPUT`\n"
            "2. Digite sua região (ex: `US`, `EU`, `KR`, `CN`, `TW`)\n"
            "3. Depois, digite seu servidor e seu nick (ex: `azralon nomepersonagem`)\n\n"
            "**⚙️ Comandos adicionais que você pode usar:**\n"
            "`-s`, `-scaling`: Calcula quais stats são mais importantes para você\n"
            "`-fs`, `-fightstyle`: Define o estilo de luta. (ex: Patchwerk, DungeonSlice)\n"
            "`-fl`, `-fightlength`: Define a duração do combate em segundos (ex: `300` segundos)\n"
            "`-ec`, `-enemycount`: Define o número de inimigos/bosses (padrão: 1)\n"
            "`-nb`: Executa a simulação sem buffs de raid\n"
            "`-v`, `-version`: Define a versão do SimulationCraft (padrão: nightly)\n\n"
            "**📊 Estilos válidos para `-fs` (fightstyle):**\n"
            "- `Patchwerk`: Luta estática, sem movimento\n"
            "- `DungeonSlice`: Simulação com múltiplos alvos, cenário de masmorra\n"
            "- `TargetDummy`: bater em um boneco de treino\n"
            "- `ExecutePatchwerk`: Luta com dano focado em *execute* (últimos % do boss)\n"
            "- `LightMovement`: Combate com um pouco de movimento\n"
            "- `HeavyMovement`: Muito movimento durante a luta\n"
            "- `HecticAddCleave`: Situação caótica com vários adds aparecendo"
        )
    elif escolha == "jeeves":
        await ctx.send(
            "**📘 Guia de uso do Jeeves:**\n\n"
            "🛠️ Jeeves é um bot completo para WoW, com suporte a personagens, recrutamento e utilidades de servidor.\n\n"
            "**👤 Conta e personagens:**\n"
            "- `/authorize`: Liga sua conta Battle.net ao Jeeves.\n"
            "- `/characters view`: Mostra seus personagens ou os de outro usuário.\n"
            "- `/characters set-main`: Define seu personagem principal.\n"
            "- `/characters hide` / `unhide`: Esconde ou mostra personagens da sua conta.\n"
            "- `/wowtoken`: Mostra o valor do token em tempo real.\n\n"
            "**🧑‍🤝‍🧑 Recrutamento:**\n"
            "- `/recruitment find-players`: Busca jogadores procurando guildas.\n"
            "- `/recruitment post`: Anuncia sua guilda para recrutar membros.\n"
            "- `/recruitment update`: Atualiza as informações da sua guilda.\n\n"
            "**📡 Monitoramento e alertas:**\n"
            "- `/realm-alerts`: Ativa alertas quando servidores do WoW ficarem offline/online.\n"
            "- `/servers`: Mostra servidores WoW relacionados e seus convites.\n\n"
            "**🎭 Papéis e permissões:**\n"
            "- `/roles add`: Usuários se atribuem papéis pré-definidos.\n"
            "- `/reaction-role add/view/remove`: Configura papéis por reação (emoji).\n\n"
            "**⚙️ Configuração:**\n"
            "- No painel web do Jeeves você pode ajustar região padrão, canal de M+, prefixos e mais."
        )
    else:
        await ctx.send("❌ Opção inválida. Tente novamente com: `jeeves` ou `raidbots`.")


bot.run(os.getenv("DISCORD_TOKEN"))