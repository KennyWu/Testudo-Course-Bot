import discord
from RetrieveData import Retrieve
from discord.ext import tasks, commands
import json

discord.utils.setup_logging()

SEMSESTER = "202301"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(allowed_mentions=discord.AllowedMentions(
    everyone=True), command_prefix='!', intents=intents)
data_retriever = Retrieve(semester=SEMSESTER)
courses = dict()
prev_data = dict()
channel_id = ""
with open('config.json') as f:
    f = json.load(f)


@bot.command()
async def cmds(ctx):
    await ctx.send("""add courses - !course courseName sections(spaced)
delete courses/sections - !delete courseName sections(optional)
retrieve and print data - !retrieve (no args)
List courses and sections to be retrieve - !list""")


@bot.command(description='Adding multiple courses/sections')
async def course(ctx, *arg):
    global channel_id
    success = False
    async with ctx.typing():
        if len(arg) >= 2:
            success = True if add_courses(arg) else False
    if success:
        channel_id = ctx.channel.id
        retrieve_important.cancel()
        await ctx.send("Courses added Sucessfully")
        update_data()
        retrieve_important.start()
    else:
        await ctx.send("Courses weren't added for following possible reasons:")
        await ctx.send("Course not existing, Section not existing")


@bot.command()
async def delete(ctx, *arg):
    global channel_id
    success = False
    async with ctx.typing():
        if len(arg) >= 1:
            success = True if delete_courses(arg) else False
    if success:
        channel_id = ctx.channel.id
        retrieve_important.cancel()
        await ctx.send('Courses/Sections deleted')
        update_data()
        retrieve_important.start()
    else:
        await ctx.send('Courses/Sections not successfully deleted')


@bot.command()
async def retrieve(ctx):
    data = dict()
    async with ctx.typing():
        data = data_retriever.retrieve()
    if len(data) != 0:
        for course in data:
            course_str = '**COURSE: ' + course + '**'
            for section in data[course]:
                course_str += '\n\tSECTION: ' + section
                course_str += '\n\t\tTIME: ' + data[course][section][0]
                course_str += '\n\t\tOPENINGS: ' + data[course][section][1]
                course_str += '\n\t\tWAITLIST: ' + data[course][section][2]
            await ctx.send(course_str)
    else:
        await ctx.send('Courses not found')


@bot.command()
async def list(ctx):
    courses = data_retriever.course_selection
    if len(courses) != 0:
        for course in courses:
            list_course = 'COURSE: ' + course + "\n\tSECTIONS:"
            for section in courses[course]:
                list_course += '\n\t\t' + section
            await ctx.send(list_course)
    else:
        await ctx.send('No courses added')


# TODO compare and contrast between data points
@tasks.loop(minutes=10)
async def retrieve_important():
    global channel_id
    data = dict()
    data = data_retriever.retrieve()
    channel = bot.get_channel(channel_id)
    changes = set()
    if len(data) != 0:
        for course in data:
            course_str = '**COURSE: ' + course + '**'
            for section in data[course]:
                time = data[course][section][0]
                openings = int(data[course][section][1])
                waitlist = int(data[course][section][2])
                str_changes = compare(
                    course, section, openings, time, "openings")
                str_changes += "\n" + \
                    compare(course, section, openings, time, "openings")
                if not str_changes:
                    changes.add(str_changes)
        if len(changes) != 0:
            await channel.send('@everyone\n')
            for change in changes:
                await channel.send(change + "\n")
        else:
            await channel.send("No changes found")
    else:
        await channel.send('No courses found')

#ctx, course, section, to_compare, time, comparison_type


def compare(course, section, to_compare, time, comparison_type):
    global prev_data
    orig_val = 0
    if comparison_type == "waitlist":
        orig_val = int(prev_data[course][section][1])
    else:
        orig_val = int(prev_data[course][section][2])
    comparison = course + " has "
    flag = False
    if orig_val > to_compare:
        flag = True
        comparison += "increased "
    elif orig_val < to_compare:
        flag = True
        comparison += "decreased "
    if flag:
        comparison += (f"in {comparison_type} for section {section}, " +
                       f" {time}, from {orig_val} {comparison_type} to {to_compare} {comparison_type}")
    else:
        comparison = ""
    return comparison


def update_data():
    global prev_data
    prev_data = data_retriever.retrieve()


def add_courses(args: tuple):
    section = set()
    course = args[0]
    for sections in args[1::]:
        section.add(sections)
    if not data_retriever.add(course=course, section=section):
        return False
    else:
        return True


def delete_courses(arg):
    if len(arg) >= 2:
        section = set()
        course = arg[0]
        for sections in arg[1::]:
            section.add(sections)
        return data_retriever.delete(course=course, section=section)
    else:
        return data_retriever.delete(course=arg[0])


bot.run(f["token"])
