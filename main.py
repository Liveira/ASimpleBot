import asyncio
from datetime import timedelta
import datetime
from io import BytesIO
from random import randrange
######fallenn é gay
import discord
import json
import re
from discord import reaction
from discord.enums import Status
from discord.flags import Intents
import requests
import time
from PIL import Image
from discord.ext import commands
from discord.utils import get


bot = commands.Bot(command_prefix=['g?', 'G?'], case_insensitive=True, Intents=discord.Intents.all())
bot.remove_command("help")
epoch = datetime.datetime.utcfromtimestamp(0)
frases = [
    "Você sabia que para comprar todos os itens de cada NPC você precisaria de exatas 27 platinas,18 ouros, 73 pratas e 73 cobres?",
    "Você sabia que na versão de console tem uma chance de 1/1000 de você pegar o dobro de loot dos montros?",
    "Você sabia que durante a lua de sangue as NPCs femininas se tornam mais agressivas em suas falas? A única excessão é a Party Girl.",
    "Você sabia que o Destroyer é o segundo boss com mais vida do jogo? Perdendo apenas para Moon Lord.",
    "Você sabia que a Plantera é o boss com mais drops do jogo? Totalizando 15 drops, e o segundo boss com mais drops é a Queen Bee, com 14.",
    "Você sabia que as noites no Terraria Mobile têm duração menor do que em outras plataformas? E Quando algum Boss é invocado, é acrescentado mais tempo até o amanhecer.",
    "Você sabia que existe uma chance desconhecida do Travelling Merchant vender a Dragon Armor, Titan Armor e a Spectral Armor no console?",
    "Você sabia que na versão de PC e Console (Nova Geração) se um jogador morrer com mais de 10 ouros no inventário, sua lapide será dourada?",
    "Você sabia que o King Slime é o único Boss que toma dano em lava?",
    "Você sabia que no Halloween, o zumbi enfermeira é uma possível referência ao Coringa no final de Batman: Cavaleiro das Trevas?",
    "Você sabia que o terraria de pc possui mundos que são cerca de 35% maiores que a versão mobile?,"
    "Você sabia que o dano de queda do terraria mobile é menor do que do de pc?,"
    "Você sabia que no terraria de pc os mobs que se teleportam, como exemplo goblin sorcerer, na versão mobile eles se teleportam mais rapido,"
]
devs = [
    563448056125587457,
    678391107662381080,
    718264081982685313,
    441003064179163150
]
React = [
    ["✅", "❌"],  # Jornada Inicio! [0][1]
    []]
dadostemp=[
    ['null'],
    []
]
staffs=[
638020094076649493,
563448056125587457,
3718264081982685313,
718264081982685313,
259699324437397505,
685635634316312597
]
async def loup(loop):
        loopV = loop
        while loopV == True:
            game = discord.Game(name="G? | Fan Art feito por: https://www.youtube.com/user/jakethewird ! | Apoie o GUIDE -> g?apoie")
            await bot.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(randrange(10,30))
            game = discord.Game(name=" G? | Terraria! | Apoie o GUIDE -> g?apoie")
            await bot.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(randrange(10,30))
            game = discord.Game(name="G? | Apenas ajudando | Apoie o GUIDE -> g?apoie")
            await bot.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(randrange(10,30))
class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_ready(self):
        print("O Guia está pronto para começar o trabalho!")
        await loup(True)
        global chname
        with open("dat.json", "r") as f:
            pvars = json.load(f)
        if "chname" in pvars:
            chname = pvars['chname']
        else:
            pvars['chname'] = 0
            with open("dat.json", "w") as f:
                json.dump(pvars, f)
        

    @commands.Cog.listener()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def on_message(self, message):
        if message.author.bot != True:
            naotemconta = await criar_conta(message.author)
            users = await pegar_os_dados_la()
            xp = users[str(message.author.id)]["xp"]
            msgs = users[str(message.author.id)]["msgs"]
            counter = users[str(message.author.id)]["counter"]
            level = users[str(message.author.id)]["level"]
            old = users[str(message.author.id)]["old"]
            try:
                noping = users[str(message.author.id)]["noping"]
            except KeyError:
                noping = 0
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - users[str(message.author.id)]['xp_time']
            if time_diff >= 30:
                xp += randrange(1,10)
                users[str(message.author.id)]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
            if xp > (old + 500) * (level + 1):
                if noping == 0:
                    await message.channel.send("Parabéns, " + message.author.mention + ", você passou de nível!")
                else:
                    await message.channel.send("Parabéns, " + message.author.name + ", você passou de nível!")
                level += 1
                old = xp
                xp += 1
            if not message.content.startswith("g?"):
                msgs += 1
            users = await dumpall(message.author, users, xp, old, level, counter, msgs)
            users[str(message.author.id)]['name'] = message.author.name + '#' + message.author.discriminator
            with open("stats.json", "w") as f:
                json.dump(users, f)
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Aguarde {int(int(error.retry_after)/ 60 / 60)} Horas para usar o comando novamente")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Está faltando `{error.param}`, use o comando novamente com o argumento!")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Esse comando não existe...")
        elif isinstance(error,commands.NoPrivateMessage):
            await ctx.send("Esse comando não é pra ser executado aqui...")
        elif isinstance(error,commands.TooManyArguments):
            await ctx.send("Você colocou mais argumentos do que o esperado")
        elif isinstance(error,commands.MemberNotFound):
            await ctx.send("Esse membro não existe")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Você não tem permissão... Permissões necessarias: {error.missing_perms}")
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send(f"Cargo {error.argument} não encontrado")
    @commands.Cog.listener()
    async def on_member_join(self,member):
        print(f'Esse puto entro: {member.name}')    
bot.add_cog(Eventos(bot))
@bot.event
async def on_member_update(after,before):
        print('a')
async def criar_conta(user):
    users = await pegar_os_dados_la()
    if str(user.id) in users:
        return False  # retorna False se a conta existir
    elif user.bot == False:
        users[str(user.id)] = {"name": user.name + "#" + user.discriminator, "level": 0, "date": time.localtime(),
                               "counter": 0, "xp": 0, "old": 0, "msgs": 0, "noping": 1, "warns": 0,
                               "description": "Eu sou uma pessoa comum!", "rep": 0,"badges":[],'Ficha':{},"xp_time":0}
        # criar um novo user com tudo zerado, exceto o noping, que quando ativado(1), não marca o usuário quando ele sobe de level
    else:
        return False
    with open("stats.json", "w") as f:
        json.dump(users, f, indent=4)  # salvar tudo no arquivo
    return True  # retorna True se a conta for criadaaaaaaaaaa
async def pegar_os_dados_la():
    with open("stats.json", "r") as f:
        return json.load(f)
async def dadosCargo():
    with open("dat.json", "r") as f:
        return json.load(f)
async def dumpall(user, users, xp, old, level, counter, msgs):
    users[str(user.id)]["xp"] = xp
    users[str(user.id)]["old"] = old
    users[str(user.id)]["msgs"] = msgs
    users[str(user.id)]["level"] = level
    users[str(user.id)]["counter"] = counter
    return users
async def dadosBadge():
    with open('badges.json','r') as f:
        return json.load(f)
async def criar_badge(nome,emoji,desc,id):
    dados = await dadosBadge()
    if nome in dados:
        return 'Badge já existente'
    else:
        dados[nome] = {
            'emoji':emoji,
            'desc':desc,
            'uses':0,
            'id':id
        }
        with open("badges.json", "w") as f:
            json.dump(dados, f, indent=4)
        return 'Badge Criada'
################################################# ÚTIL
class wiki(commands.Cog):
    @commands.command(name="Wiki", category="Util")
    async def wiki(self, ctx, *, name=None):
        if name != None:
            name = re.sub(" ", "_", name)
            await ctx.send("Aqui esta oque você pediu -> : -> https://terraria.gamepedia.com/" + name)
            await ctx.send(
                "Se você digitar o nome errado, ele provavelmente não funcionará... Tenha certeza que o nome está certo antes de dar esse comando.")
        else:
            await ctx.send(
                "Hmmm... Parece que você não informou o tipo, mas ok, aqui está o link da wiki! -> https://terraria.gamepedia.com")
bot.add_cog(wiki(bot))
class curiosidades(commands.Cog):
    @commands.command(aliases=['curiosidades'])
    async def curiosidade(self, ctx):
        await ctx.send(frases[randrange(0, len(frases))])
bot.add_cog(curiosidades(bot))
################################################# OUTROS
class say(commands.Cog):
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)
bot.add_cog(say(bot))
'''class teste(commands.Cog):
    @commands.command()
    async def teste(self, ctx):
        url = requests.get(ctx.author.avatar_url)
        avatar = Image.open(BytesIO(url.content))
        # fonte = ImageFont.truetype('fontes/andy-bold.ttf', 20)
        avatar.save('avatar.png')
        file = discord.File(open('avatar.png', 'rb'))
        await ctx.send(file=file)
bot.add_cog(teste(bot))'''
class ping(commands.Cog):
    @commands.command()
    async def ping(self, ctx):
        ping = bot.latency * 1000
        await ctx.send(f"Meu ping é {int(ping)}")
bot.add_cog(ping(bot))
class ddfrag(commands.Cog):
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ddfrag(self, ctx):
        dados = await pegar_os_dados_la()
        cont = 0
        contb = 0
        msg=''
        msg = await ctx.send("<a:loading:781520172707217438> Aguarde...")
        async for i in ctx.guild.fetch_members(limit=None):
            if str(i.id) in dados or i.bot == True:
                contb +=1
                pass
            else:
                cont += 1
                await criar_conta(i)
        await msg.edit(content=f"Contas criadas {cont}, e {contb} foram ignorados.")
        await msg.add_reaction(React[0][0])   
bot.add_cog(ddfrag(bot))
class dados(commands.Cog):
    @commands.command()
    async def dados(self, ctx, Qtd_lados):
        await ctx.send("Oh, Aqui está o resultado " + str(randrange(0,int(Qtd_lados))))
bot.add_cog(dados(bot))
################################################# RANKKKKK
class top(commands.Cog):
    @commands.command()
    async def top(self, ctx):
        dados = await pegar_os_dados_la()
        dictF = {}
        dadosxp = []
        msg = ""
        pos = 0
        num = 0
        embed = discord.Embed(title="Rank", color=ctx.author.color)
        for i in dados:
            num+=1
            xpatual = dados[i]["xp"]
            print(xpatual)
            nome_atual = dados[i]["name"]
            dictF[xpatual] = nome_atual
            print(dictF[xpatual])
            dadosxp.append(dados[i]["xp"])
        Expe = sorted(dictF, reverse=True)
        for x in Expe:
            pos += 1
            msg = msg + "\n[" + str(pos) + "](" + dictF[x] + ") - " + str(x) + "\n"
            if pos >= 10:
                break
        embed.add_field(name="POS       |      NOME      |        XP    ", value=f"```markdown\n{msg}```")
        await ctx.send(embed=embed)
bot.add_cog(top(bot))
class perfil(commands.Cog):

    @commands.group(name="perfil", aliases=['profile', 'user', 'usuario'], invoke_without_command=True)
    async def cmd_perfil(this, ctx, user: discord.Member = None):
        user = user or ctx.author
        if user.id == 779365780848377856:
            await botinfo.botinfo(this,ctx)
        else:
            dados = await pegar_os_dados_la()
            msg=""

            if user.id in devs:
                embed = discord.Embed(title=user.name + " <a:Dev:781562137483018290> ", description="Seu XP e Mensagens serão mostrados aqui!", color=user.color)
            else:
                embed = discord.Embed(title=user.name, description="Seu XP e Mensagens serão mostrados aqui!", color=user.color)

            embed.set_thumbnail(url=str(user.avatar_url))
            embed.add_field(name="Nivel", value="Seu nivel: " + str(dados[str(user.id)]["level"]), inline=True)
            embed.add_field(name="XP", value="XP: " + str(dados[str(user.id)]["xp"]), inline=True)
            embed.add_field(name="Mensagens", value="Quantidade de mensagens: " + str(dados[str(user.id)]["msgs"]),
                            inline=True)
            embed.add_field(name="Sobre-mim", value=str(dados[str(user.id)]["description"]), inline=True)
            embed.add_field(name="Reputação", value=str(dados[str(user.id)]["rep"]), inline=True)
            for i in range(len(dados[str(user.id)]["badges"])):
                
                msg = msg + dados[str(user.id)]['badges'][i] + " "
            embed.add_field(name="Insignias", value="-> " + msg, inline=True)

            embed.set_footer(
                text="Você sabia que dá para alterar o \"Sobre mim?\", é muito simples, basta somente colocar g?perfil config desc <nova desc>",
                icon_url='https://cdn.discordapp.com/emojis/586639474726010920.png?v=1')
            await ctx.send(embed=embed)

    @cmd_perfil.command(name="config", aliases=['conf', 'configurar', 'configuração', 'cfg', 'mudar'])
    async def config(this, ctx, tipo, *, msg):
        dados = await pegar_os_dados_la()
        if tipo == 'desc' or 'descrição' or 'description' or 'sobre' or 'sobre-mim':
            dados[str(ctx.author.id)]["description"] = msg
            await ctx.send("\"Sobre-mim\" alterada para: " + msg)
            with open("stats.json", "w") as f:
                json.dump(dados, f)
bot.add_cog(perfil(bot))
class rep(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def rep(self, ctx, user: discord.Member):
        
        if user.id == ctx.author.id:
            await ctx.send("Hahahaha! Muito engraçado você, Não pode dar reputação para você mesmo, como aviso você vai esperar 1 dia pra usar esse comando denovo!") 
        else:
            dados = await pegar_os_dados_la()
            ant = dados[str(user.id)]["rep"]
            dados[str(user.id)]["rep"] += 1
            with open('stats.json', 'w') as f:
                json.dump(dados, f)
            embed = discord.Embed(title="Reputação",
                                description=f"Você acabou de dar um ponto de reputação para {user.display_name}!")
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Antes", value=ant)
            embed.add_field(name="Depois", value=dados[str(user.id)]["rep"])
            await ctx.send(embed=embed)
bot.add_cog(rep(bot))
################################################# BOTTTTTTTTTTTTTTTTTTT
class userinfo(commands.Cog):
    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title=ctx.author.name, color=ctx.author.color)
        embed.set_author(name="Informações de usuario")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Nome", value=f"`{user.name}#{user.discriminator}` ", inline=True)
        embed.add_field(name="ID", value=f"`{str(user.id)}`", inline=True)
        embed.add_field(name="Conta criada há", value=user.created_at, inline=True)
        embed.add_field(name="Entrou há", value=user.joined_at, inline=True)
        # embed.add_field(name="Descrição", value=dados[str(ctx.author.id)]["description"], inline=True)
        embed.set_footer(text="Dica: Para ver informações de outros usarios: g?userinfo [ID/MENTION]!")
        await ctx.send(embed=embed)
bot.add_cog(userinfo(bot))
class botconfig(commands.Cog):
    @commands.command()
    async def botConfig(self, ctx, role: discord.Role):
        global rol
        rol = {"Role": f"{role}"}
        await ctx.send("Role setada com sucesso!")
        with open("dat.json", "w") as f:
            json.dump(rol, f)
bot.add_cog(botconfig(bot))
class botinfo(commands.Cog):
    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title=" <:Guide:779713033135325204>  Bem vindo as minhas informações",
                              description="As informações do guia... Aka (eu)")
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.add_field(name="Quem me criou?", value="Gustavo/Nightter")
        embed.add_field(name="Quando eu nasci?", value="20/11/2020")
        embed.add_field(name="Como eu fui criado?",
                        value="Eu fui criado apartir da linguagem de programação [Python!](https://python.org) Tudo aqui foi feito do ZERO, feito pelo dono, **Nightter** ")
        embed.add_field(name="Quem fez a foto de perfil?", value="[JakeTheWird](https://www.youtube.com/user/jakethewird), Lembrando, essa foto não é direito nosso")
        await ctx.send(embed=embed)
bot.add_cog(botinfo(bot))
class help(commands.Cog):
    @commands.command()
    async def help(self, ctx):
        global staffs
        embed = discord.Embed(title=ctx.author.name, description="Aqui está a lista de comandos que podem ser úteis!",
                              color=ctx.author.color)
        embed.add_field(name="Útil",
                        value="```Wiki``` -> Dá o link da wiki com as caracteristicas que você digitou!\n```Curiosidade``` -> Manda uma curiosidade aleatoria sobre Terraria\n")
        embed.add_field(name="Usuarios",
                        value="```Perfil``` -> Mostra o seu perfil, com descrição, subcomandos (config desc)\n```Top``` -> Manda uma lista com os 10 com mais XP do servidor!\n```Userinfo``` -> Manda uma mensagem contendo todas as informações do seu usuario ou um que você digitar!\n")
        if ctx.author.id in staffs:
            embed.add_field(name="Moderação", value="```Warn``` -> Da warn em usuarios\n```Mute``` -> Muta os usuarios\n```Kick``` -> kicka os usuarios\n```Ban``` -> bani os usuarios\n```Unban``` -> Desbani um usuario\n```Reset``` -> Reseta o xp de todo mundo ou de uma pessoa em especifico")
        else:
            embed.add_field(name="Moderação", value="```Comandos Invisiveis```")
        embed.add_field(name="Outros",value="```Dados``` -> Role o dado e teste sua sorte!\n```Ping``` -> Bot está demorando para responder? Verifique o ping!\n```Badge``` -> Veja como conseguir uma badge que você queira! Ou saber quantas pessoas tem aquela determinada badge")
        embed.set_footer(
                text="Você sabia que eu tenho mais de 20 comandos?",
                icon_url='https://cdn.discordapp.com/emojis/586639474726010920.png?v=1')
        await ctx.send(embed=embed)
bot.add_cog(help(bot))
class apoie(commands.Cog):
    @commands.command()
    async def apoie(this,ctx):
        embed = discord.Embed(title='Me apoie', description='Olá, você quer me apoiar? Aaaa que legal! Não é gratis ficar online toda hora né, preciso de ajuda as vezes')
        embed.add_field(name="Formas de pagamento", value="[PayPal](https://www.paypal.com/donate?hosted_button_id=B377C26RX9ATC)!")
        embed.set_footer(text='TODO Dinheiro das doações será destinado ao pagamento da HOST, não é gratis, então precisamos de ajuda para pagar o host')
        await ctx.send(embed=embed)
bot.add_cog(apoie(bot))
################################################# MODERAÇÃAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOOOOOOOOOOOOOOOOOOOOOOOOO
class ban(commands.Cog):
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="None"):
        await ctx.send("Usuario Banido!")
        await user.send("Você foi **BANIDO** do Terraria PT-BR, Motivo: " + reason)
        await user.ban()
bot.add_cog(ban(bot))
class unban(commands.Cog):
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int, *, reason="None"):
        user = await bot.fetch_user(id)
        if user == None:
            await ctx.send("Informe o usuario que deseja banir")
        else:
            await ctx.send("Usuario desbanido!")
            await ctx.guild.unban(user)
bot.add_cog(unban(bot))
class kick(commands.Cog):
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="None"):
        await ctx.send("Usuario Kickado!")
        await user.send("Você foi **Kickado**!, Motivo: " + reason)
        await user.kick()
bot.add_cog(kick(bot))
class mute(commands.Cog):
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, *, Reason="None"):
        await ctx.send("Usuario mutado")
        data = await dadosCargo()
        role = get(ctx.guild.roles, name=data["Role"])
        await user.add_roles(role, reason=Reason)
        await user.send("Você foi **Mutado**!, Motivo: " + Reason)
bot.add_cog(mute(bot))
class warn(commands.Cog):
    @commands.group(name='warn', invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    async def cmdwarn(self, ctx, user: discord.Member, *, motivo='Nenhum'):
        dados = await pegar_os_dados_la()
        dados[str(user.id)]["warns"] += 1
        cont = dados[str(user.id)]["warns"]
        dados[str(user.id)]["Ficha"][cont] = {'cont':cont,'motivo':motivo}
        await ctx.send(f"Usuario {user.name} levou warn. Já é o {dados[str(user.id)]['warns']}° Aviso!")
        await user.send(user.mention + ", você foi avisado, " + str(dados[str(user.id)][
                                                                        "warns"]) + "° Aviso, motivo: " + motivo + "\n**Aviso**: Não questinou o porque do warn, o motivo está na mensagem.")
        # await ctx.send("O Usuario: " + user.mention + " foi avisado.  " + str(dados[str(user.id)]["warns"]) + "° Aviso, motivo: " + motivo)
        with open("stats.json", "w") as f:
            json.dump(dados, f)
    @cmdwarn.command(name='check')
    async def check(self,ctx,user: discord.Member):
        dados = await pegar_os_dados_la()
        msg=''
        embed = discord.Embed(title=f'Ficha "Criminal" do {user.name}',description='Isso mostrara tudo sobre o membro a seguir :+1:')
        embed.add_field(name='Warns',value=f'Quantidade total de warns: {dados[str(user.id)]["warns"]}')
        for i in dados[str(user.id)]['Ficha']:
            msg = msg + '\n' + str(dados[str(user.id)]['Ficha'][i]['cont']) + '  -  ' + dados[str(user.id)]['Ficha'][i]['motivo']
        embed.add_field(name='Historico de warns',value='```\n'+msg+'```')
        await ctx.send(embed=embed)
bot.add_cog(warn(bot))
class reset(commands.Cog):
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def reset(this,ctx,user: discord.Member=None):
        cont=0
        if user == None:
            embed = discord.Embed(title="Você tem certeza?", description="Reaja :white_check_mark: para resetar o XP de TODO MUNDO!, caso queria resetar o xp de um unico membro, g?reset <usuario>!")
            async for i in ctx.guild.fetch_members(limit=None):
                cont += 1
            embed.add_field(name=f"Você ira resetar o xp de {cont} membros",value="Você tem certeza?")            
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(React[0][0])
            await asyncio.sleep(20)
            await msg.edit(content=f":clock{randrange(1,12)}: Tempo de inatividade execidido, excluindo mensagem")
            await asyncio.sleep(5)
            await msg.delete()
    @commands.Cog.listener()
    async def on_reaction_add(this,react,user):
        dados = await pegar_os_dados_la()
        if user.bot == True:
            return
        else:        
            guid = user.guild
            if react.emoji == React[0][0]:
                msg = await react.message.channel.send("<a:loading:781520172707217438>  Aguarde...")
                async for i in guid.fetch_members(limit=None):
                        if i.bot != True:
                            dados[str(i.id)]["xp"] = 0
                            dados[str(i.id)]["level"] = 0
                            dados[str(i.id)]["msgs"] = 0
                            with open('stats.json','w') as f:
                                json.dump(dados,f)
                await msg.edit(content="Pronto!")
                await asyncio.sleep(5)
                await msg.delete()
bot.add_cog(reset(bot))
class badges(commands.Cog):
    @commands.group(name="badge", aliases=['bad', 'badg', 'bdg'], invoke_without_command=True)
    async def cmdBadge(this,ctx):
        embed =  discord.Embed(title=':speech_balloon: Comando BADGE',description='```g?badge```\n\nbadge é insingnia em inglês, alguns usuarios podem ter badges, caso ele merecer ele pode ganhar uma badge que ficara no perfil dele!\n\n:question: Como usar: `g?badge <tipo>`\n Aqui está os tipos que você pode usar!:\n\n`g?badge list` -> Lista todas as badges existentes!\n`g?badge info <nome da badge>` -> Mostra informações sobre a badge que você digitou!\n\n:globe_with_meridians: Outros Nomes:\n`g?bad`,`g?bdg`')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @cmdBadge.command(name='add')
    @commands.has_permissions(kick_members=True)
    async def add(self,ctx,user: discord.Member,badge):
        Varbadges = await dadosBadge()
        dados = await pegar_os_dados_la()
        if badge in Varbadges:
            dados[str(user.id)]["badges"].append(Varbadges[badge]['emoji'])
            await ctx.send(f"O Usuario: {user.name} recebeu uma insignia! -> {Varbadges[badge]['emoji']}")
            Varbadges[badge]['uses'] += 1
        else:
            await ctx.send("Badge invalida, veja a lista de badges em g?badges list")
            return
        with open('stats.json','w') as f:
            json.dump(dados,f)
        with open('badges.json','w') as f:
            json.dump(Varbadges,f)
    @cmdBadge.command(name='list', aliases=['listar'])
    async def listar(self,ctx):
        dados = await dadosBadge()
        msg=''
        for i in dados:
            print(i)
            msg = msg + '\n' + dados[i]['emoji'] + ' - ' + i + '\n'
        embed = discord.Embed(title='Lista de badges',description='Listei todas as badges!')
        embed.add_field(name='Badges',value=f'{msg}')
        await ctx.send(embed=embed) 
    @cmdBadge.command(name='new',aliases=['novo'])
    async def novo(self,ctx,emoji: discord.Emoji,nome,*,desc):
        VarBadges = await dadosBadge()
        status = await criar_badge(nome,f'<:{emoji.name}:{emoji.id}>',desc,emoji.id)
        await ctx.send(status)
    @cmdBadge.command(name='info')
    async def info(self,ctx,nome):
        dados = await dadosBadge()
        if nome in dados:
            EID = dados[nome]['id']
            emojiss = await ctx.guild.fetch_emoji(EID)
            embed = discord.Embed(title='Informação da badge',description='Aqui sera mostrado a informação da badge que você digitou')
            embed.add_field(name='Nome',value=nome)
            embed.add_field(name='Descrição',value=dados[nome]['desc'])
            embed.add_field(name='Qtd. de pessoas que tem essa badge',value=dados[nome]['uses'])
            embed.set_thumbnail(url=emojiss.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Nome invalido')
    @cmdBadge.command(name='remove')
    async def remove(self,ctx,user: discord.Member,index):
        dados = await pegar_os_dados_la()
        try:
            ant = dados[str(user.id)]['badges'][int(index) - 1]
            del(dados[str(user.id)]['badges'][int(index) - 1])
            await ctx.send(f'Badge removida -> {ant}')
            with open('stats.json','w') as f:
                json.dump(dados,f)
        except IndexError:
            await ctx.send('Index inexistente')
bot.add_cog(badges(bot))
class unwarn(commands.Cog):
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, user: discord.Member, *, motivo='Nenhum'):
        dados = await pegar_os_dados_la()
        cont = str(dados[str(user.id)]["warns"])
        if cont == '0':
            cont = '1'
        dados[str(user.id)]["warns"] -= 1
        del dados[str(user.id)]["Ficha"][str(cont)]
        await ctx.send(f"O Warn do Usuario {user.name} foi removido, agora ele tem {dados[str(user.id)]['warns']}° Avisos!")
        await user.send(user.mention + ", Seu warn foi retirado. " + str(dados[str(user.id)]["warns"]) + "° Aviso, motivo: " + motivo + "\n**Aviso**: Não questinou o porque do warn, o motivo está na mensagem.")
        # await ctx.send("O Usuario: " + user.mention + " foi avisado.  " + str(dados[str(user.id)]["warns"]) + "° Aviso, motivo: " + motivo)
        with open("stats.json", "w") as f:
            json.dump(dados, f)
bot.add_cog(unwarn(bot))
#10 a 18? 10+11+12+13+14+15+16+17+18 = 126/8 = 15,75

"""
@bot.command()
@commands.dm_only()
async def modmail(ctx, tipo, *, mensagems):
    tipo = tipo.lower()
    if tipo == "denuncia" or "report":
        channel = bot.get_channel(776197504378732555)
        embed = discord.Embed(description="Para responder uma chamada, g?responder <id do usuario> <mensagem>")
        embed.add_field(name="Conteudo", value=mensagems)
        embed.add_field(name="Tipo", value="Denuncia")
        embed.set_footer(text="Usuario: " + ctx.author.name + " | ID da Mensagem  -> " + str(ctx.author.id))
        await channel.send(embed=embed)
        embed = discord.Embed(title="Lembre-se, as mensagens DEVEM ser formais e explicativas!")
        embed.add_field(name="Mensagem", value=mensagems)
        embed.add_field(name="Tipo", value="Denuncia")
        embed.set_footer(text="A Carta foi mandada, Aguarde resposta")
        await ctx.send(embed=embed)

    elif tipo == "sugestão" or "sugestion":
        channel = bot.get_channel(776197504378732555)
        embed = discord.Embed(description="Para responder uma chamada, g?responder <id da mensagem> <mensagem>")
        embed.add_field(name="Conteudo", value=mensagems)
        embed.add_field(name="Tipo", value="Denuncia")
        embed.set_footer(text="Usuario: " +ctx.author.name+" ID da Mensagem  -> " + str(ctx.author.id))
        await channel.send(embed=embed)
        embed = discord.Embed(title="Lembre-se, as mensagens DEVEM ser formais e explicativas!")
        embed.add_field(name="Mensagem", value=mensagems)
        embed.add_field(name="Tipo", value="Denuncia")
        embed.set_footer(text="A Carta foi mandada, Aguarde resposta")

        await ctx.send(embed=embed)
@bot.command()
async def responder(ctx,id,*,mensagem):
    user = bot.get_user(int(id))
    embed = discord.Embed()
    embed.add_field(name="Resposta",value=mensagem)
    embed.set_footer(text="Para criar uma nova carta g?modmail <tipo> <mensagem>")
    await ctx.send("Mensagem enviada para: " + user.name)
    await user.send(embed=embed)
@bot.command()
@commands.dm_only()
async def ajudamodmail(ctx):
    embed = discord.Embed(title="Ajuda ModMail!",description="Aqui serão mostrado a ajuda dos comandos de Modmail!")
    embed.add_field(name="Comandos",value="```g?modmail```\n`g?modmail <tipo> <- Tipos: Sugestão, Denuncia e ajuda! <Mensagem>`\n  ")
    await ctx.send(embed=embed)
"""
'''async def MensagemPadrao(ctx):
    await ctx.send("Ops... Parece que você não tem um perfil, Para criar, use o comando g?start! ")
@bot.command()
async def start(ctx):
    global React
    mensagem = await ctx.send("Você quer realmente começar nessa jornada? ")
    await mensagem.add_reaction(React[0][0])
    await mensagem.add_reaction(React[0][1])
@bot.command()
async def wallet(ctx,user: discord.Member=None):
    dados = await dadosEconomia()
    print(dados)
    if user == None:
       if str(ctx.author.id) in dados:
           embed = discord.Embed(title=ctx.author.display_name, color=0xff0000)
           embed.set_author(name="Informações de usuario")
           embed.set_thumbnail(url=ctx.author.avatar_url)
           embed.add_field(name="Carteira", value="Poupança: " + str(dados[str(ctx.author.id)]["Money"]) + "/500000",inline=True)
           embed.set_footer(text="Dica: Para ver a carteira de outros usarios: g?wallet [ID/MENTION]")
           await ctx.send(embed=embed)
       else:
           await MensagemPadrao(ctx)
    else:
        if str(user.id) in dados:
            embed = discord.Embed(title=user.display_name, color=0xff0000)
            embed.set_author(name="Informações de usuario")
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Carteira", value="Poupança: " +str(dados[str(user.id)]["Money"]) +  "/500000", inline=True)
            embed.set_footer(text="Dica: Para ver a carteira de outros usarios: g?wallet [ID/MENTION]")
            await ctx.send(embed=embed)

            await ctx.send("")

        else:
            await MensagemPadrao(ctx)
'''
################## TO DO ########################
'''
            Concluido:
            -XP-
            Comandos de XP
            Warn
            Comandos de ajuda do bot ( Terraria )
            Perfil -=-=-= Em Andamento
            Quando alguém tomar warn/mute/ ban etc, mandar uma dm, para que a gente use o sistema de moderação nos chats da staff
            modmail
            botinfo
            
            A fazer:
            melhorar o comando help
            
            Semana:
    
            
            
            Ideias:
            

'''
bot.run(TOKEN UwU)
