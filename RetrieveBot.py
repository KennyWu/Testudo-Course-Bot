# This example requires the 'message_content' intent.

import discord
from RetrieveData import Retrieve
from discord.ext import tasks, commands

discord.utils.setup_logging()

SEMSESTER = "202301"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
data_retriever = Retrieve(semester=SEMSESTER)
courses = dict()


@bot.command()
async def cmds(ctx):
    await ctx.send("""add courses - !course courseName sections(spaced)
delete courses/sections - !delete courseName sections(optional)
retrieve and print data - !retrieve (no args)
List courses and sections to be retrieve - !list""")


@bot.command(description='Adding multiple courses/sections')
async def course(ctx, *arg):
    success = False
    async with ctx.typing():
        if len(arg) >= 2:
            success = True if add_courses(arg) else False
    if (success):
        await ctx.send("Courses added Sucessfully")
    else:
        await ctx.send("Courses weren't added for following possiible reasons:")
        await ctx.send("Course not existing, Section not existing")


@bot.command()
async def delete(ctx, *arg):
    success = False
    async with ctx.typing():
        if len(arg) >= 1:
            success = True if delete_courses(arg) else False
    if success:
        await ctx.send('Courses/Sections deleted')
    else:
        await ctx.send('Courses/Sections not successfully deleted')

# TODO - finish retrieve and looping method - process info


@bot.command
async def retrieve(ctx, *arg):
    await ctx.send('hello')


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


bot.run('OTMxNDIyNzUxMzA5MzMyNTYw.GNOTJH.6vG18RHSbNRTrG-c8mZr29OuhYcsUnHSFQdoQs')
