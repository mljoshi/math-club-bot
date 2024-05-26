import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import asyncpraw
import datetime
import asyncio
from better_profanity import profanity
from io import BytesIO
from PIL import Image
from fractions import Fraction
from dotenv import load_dotenv
# Local files:
from ocrtext import image_to_text
import math_evaluations
import re
import os
import sys

load_dotenv()
TOKEN: str = os.getenv('TOKEN')
CLIENT_ID: str = os.getenv('CLIENT_ID')
CLIENT_SECRET: str = os.getenv('CLIENT_SECRET')
USER_NAME: str = os.getenv('USER_NAME')
PASSWORD: str = os.getenv('PASSWORD')

client = commands.Bot(command_prefix = '.', intents = nextcord.Intents.all())

reddit = asyncpraw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, username = USER_NAME, password = PASSWORD, user_agent = "Python")

# daily_meme_channel_id = 1141598793897345024 # test server meme channel
# server_id = 727275619343269970 # test server id

def img_to_discord(img):
    bytes = BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)
    discord_file = nextcord.File(bytes, filename="image.png")
    return discord_file

def code_blockify(str):
    # Code blocks in Discord are indicated by a `
    new_str = "`" + str + "`"
    return new_str

def restart_bot():
    python = sys.executable
    script = os.path.abspath(__file__)
    os.execl(python, python, f'"{script}"')

def is_input_bad(input_list=None):
    if input_list is None:
        input_list = [""]
    for user_input in input_list:
        if not re.match(r'^[0-9\+\-\*\/\(\)\s\.,a-z^]+$', user_input, re.IGNORECASE):
            return True
    return False

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.Game('Cool Math Games'))
    print("Bot is ready")
    """print(client.guilds)
    for guild in client.guilds:
        print([channel for channel in guild.channels])
        """

@client.event
async def on_message(message):
    if isinstance(message.channel, nextcord.DMChannel):
        return # Ignore DMs
    await client.process_commands(message)

@client.command()
@commands.has_permissions(administrator = True)
async def restart(ctx):
    await ctx.send("Restarting")
    restart_bot()

@client.command()
@commands.has_permissions(administrator = True)
async def kill_bot(ctx):
    await ctx.send("Killing")
    exit()

@client.command()
async def meme(ctx, num_memes = 1): # Add checks for NSFW outside of Reddit's flag in future (with an AI library?)
    subreddit = await reddit.subreddit("mathmemes")
    memes = num_memes
    if (num_memes > 10): # cap out at 10 memes
        memes = 10
    checked_arr = [0, 1] # includes 0 and 1 so that it skips 0 and 1 on the first iteration of the for loop (pinned meme), could probably change this to be an int last_checked instead of a list, idr why i made it a list to begin with but i think i removed the code necessitating a list
    num_not_sent = 0
    sent = 0
    num_requests = 0 # cap out at 25 tries
    while sent < memes and num_requests < 25:
        j = 0
        hot = subreddit.hot(limit = memes + 2 + num_not_sent) # +2 since 2 pinned memes
        async for submission in hot:
            if j == checked_arr[-1] + 1:
                if 'i.redd.it' in submission.url and not profanity.contains_profanity(submission.title) and not profanity.contains_profanity(image_to_text(submission.url)) and not submission.over_18:
                    if len(submission.title) <= 256: # Discord has a cap of 256 characters in the title
                        submission_title = submission.title
                    else:
                        submission_title = submission.title[:256:]
                    emb = nextcord.Embed(title = submission_title)
                    emb.set_image(url = submission.url)
                    message = await ctx.send(embed = emb)
                    await message.add_reaction("❤️")
                    sent += 1
                else:
                    num_not_sent += 1
            j += 1
        checked_arr.append(checked_arr[-1] + 1)
        num_requests += 1

"""@client.command()
async def daily_meme(ctx):
    now = datetime.datetime.now()
    # then = now + datetime.timedelta(days = 1)
    # then.replace(hour = 10, minute = 0)
    then = now.replace(hour = 14, minute = 1) # for testing purposes set to current time
    wait_time = (then - now).total_seconds()
    await asyncio.sleep(wait_time)
    subreddit = reddit.subreddit("mathmemes")
    hot = subreddit.hot(limit = 2)
    i = 0
    count_omitted = 0
    for submission in hot:
        if i != 0:
            if profanity.contains_profanity(submission.title) or profanity.contains_profanity(image_to_text(submission.url)) or submission.over_18:
                count_omitted += 1
        i += 1
    # need to implement a way to get the first appropriate image
"""

"""
async def daily_meme():
    now = datetime.datetime.now()
    # then = now + datetime.timedelta(days = 1)
    # then.replace(hour = 10, minute = 0)
    then = now.replace(hour = 22, minute = 39) # for testing purposes set to current time
    wait_time = (then - now).total_seconds()
    await asyncio.sleep(wait_time)
    """

@client.command()
async def simplify(ctx, expression=""):
    if (is_input_bad([expression])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.simplify(expression))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Simplify: " + expression)), file=discord_file)

@client.command()
async def point_simplify(ctx, function_of_x="", c=0.0):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.point_simplify(function_of_x, c))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Simplify: " + function_of_x + " at x=" + str(c))), file=discord_file)

@client.command()
async def evaluate(ctx, expression=""):
    if (is_input_bad([expression])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.evaluate(expression))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Evaluate: " + expression)), file=discord_file)

@client.command()
async def point_evaluate(ctx, function_of_x="", c=0.0):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.point_evaluate(function_of_x, c))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Evaluate " + function_of_x + " at x=" + str(c) + ":")), file=discord_file)

@client.command()
async def intersections(ctx, function_of_x_1="", function_of_x_2=""):
    if (is_input_bad([function_of_x_1, function_of_x_2])):
        await ctx.send("Bad input")
        return
    ans = math_evaluations.intersections(function_of_x_1, function_of_x_2)
    await ctx.send(code_blockify("Intersection(s) of " + function_of_x_1 + " and " + function_of_x_2 + ": " + str(ans)))

@client.command()
async def interval_intersections(ctx, function_of_x_1="", function_of_x_2="", a="", b=""):
    if (is_input_bad([function_of_x_1, function_of_x_2, a, b])):
        await ctx.send("Bad input")
        return
    ans = math_evaluations.interval_intersections(function_of_x_1, function_of_x_2, a, b)
    await ctx.send(code_blockify("Intersection(s) of " + function_of_x_1 + " and " + function_of_x_2 + " on [" + str(a) + ", " + str(b) + "]: " + str(ans)))

@client.command()
async def partial_fraction(ctx, function_of_x=""):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.partial_fraction(function_of_x))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Partial fraction of " + function_of_x + ":")), file=discord_file)

@client.command()
async def integrate(ctx, function="x", variable_of_integration="x"):
    if (is_input_bad([function])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.integrate(function, variable_of_integration))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Integrate: " + function)), file=discord_file)

@client.command(pass_context=True)
async def integral(ctx, function="x", variable_of_integration="x"):
    await integrate(ctx, function, variable_of_integration)

@client.command()
async def def_integrate(ctx, function="x", a="0", b="1", variable_of_integration="x"):
    if (is_input_bad([function, a, b])):
        await ctx.send("Bad input")
        return
    ans = math_evaluations.def_integrate(function, a, b, variable_of_integration)
    im = math_evaluations.image_processing(ans)
    # ans = Fraction(float(ans)).limit_denominator()
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Integrate " + function + " on [" + str(a) + ", " + str(b) + "]:")), file=discord_file)

@client.command(pass_context=True)
async def def_integral(ctx, function="x", a="0", b="1", variable_of_integration="x"):
    await def_integrate(ctx, function, a, b, variable_of_integration)

@client.command(pass_context=True)
async def double_integrate(ctx, func_xy="xy", var_1="y", a1="0", b1="x^2", var_2="x", a2="0", b2="1"):
    """
    Only supports x and y
    Ex usage: ∫ 0 to 1 ∫ 0 to x^2 xcos(y) dy dx
    .double_integrate x*cos(y) y 0 x^2 x 0 1
    """
    if (is_input_bad([func_xy, a1, b1, a2, b2])):
        await ctx.send("Bad input")
        return
    ans = math_evaluations.double_integrate(func_xy, var_1, a1, b1, a2, b2)
    im = math_evaluations.image_processing(ans)
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("∫ " + a2 + " to " + b2 + " ∫ " + a1 + " to " + b1 + " " + func_xy + " d" + var_1 + " d" + var_2)), file=discord_file)

@client.command(pass_context=True)
async def double_integral(ctx, func_xy="xy", var_1="y", a1="0", b1="x^2", var_2="x", a2="0", b2="1"):
    await double_integrate(ctx, func_xy, var_1, a1, b1, var_2, a2, b2)

    
@client.command()
async def ftc2(ctx, integral_of_x="1/2*x^2", a="0", b="1"):
    if (is_input_bad([integral_of_x, a, b])):
        await ctx.send("Bad input")
        return
    ans = math_evaluations.ftc2(integral_of_x, a, b)
    im = math_evaluations.image_processing(ans)
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("F(" + b + ") - F(" + a + ") of F(x)=" + integral_of_x)), file=discord_file)

@client.command()
async def average_value(ctx, function_of_x="x", a="0", b="1"):
    if (is_input_bad([function_of_x, a, b])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.average_value(function_of_x, a, b))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Average value of " + function_of_x + " on [" + str(a) + ", " + str(b) + "]:")), file=discord_file)

"""
# Unnecessary function now that I have left_riemann
@client.command()
async def est_integral(ctx, function_of_x="", a=0.0, b=1.0, n=50):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    # Cap number of summations at 100
    if (n > 100):
        n = 100
    im = math_evaluations.image_processing(math_evaluations.est_integral(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Estimated integral of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)
    """

@client.command()
async def equal_integrals(ctx, integral_of_x_1="x", integral_of_x_2="x+1", n=20, x1=-128.0, x2=128.0, epsilon=0.0000000001): # Conditions for usage: The functions must be continuous on the closed interval [a, b] (ftc)
    if (is_input_bad([integral_of_x_1, integral_of_x_2])):
        await ctx.send("Bad input")
        return
    if (n > 200):
        n = 200
    if (x1 > x2):
        x1, x2 = x2, x1
    if (x1 < -1000):
        x1 = -1000
    if (x2 > 1000):
        x2 = 1000
    if (epsilon < 0):
        epsilon *= -1
    if (epsilon > .01):
        epsilon = .01
    elif (epsilon < 0.000000000001):
        epsilon = 0.000000000001
    message = "Checking if " + integral_of_x_1 + " and " + integral_of_x_2 + " are equal plus a constant with " + str(n) + " checks on the domain " + "(" + str(x1) + ", " + str(x2) + ") with epsilon " + str(epsilon) + "...\n"
    evaluation = math_evaluations.equal_integrals(integral_of_x_1, integral_of_x_2, n, x1, x2, epsilon)
    if (evaluation[0] == 1): # evaluation[1] only exists when evaluation[0] == 1
        message = message + "Looks equal to me, with a difference (f-g) of " + str(evaluation[1])
    elif (evaluation[0] == 0):
        message = message + "Does not appear to be equal 😬"
    else:
        message = message + "There was a TypeError during the calculation. They are likely not equal"
        if (x1 < 0):
            message = message + ". Perhaps try again with an entirely positive interval"
    await ctx.send(code_blockify(message))

@client.command()
async def left_riemann(ctx, function_of_x="x", a=0.0, b=1.0, n=10):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.left_riemann(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Left Riemann sum of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)

@client.command()
async def right_riemann(ctx, function_of_x="x", a=0.0, b=1.0, n=10):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.right_riemann(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Right Riemann sum of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)

@client.command()
async def mid_riemann(ctx, function_of_x="x", a=0.0, b=1.0, n=10):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.mid_riemann(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Midpoint Riemann sum of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)

@client.command()
async def upper_sum(ctx, function_of_x="x", a=0.0, b=1.0, n=10):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.upper_sum(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Upper sum of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)

@client.command()
async def lower_sum(ctx, function_of_x="x", a=0.0, b=1.0, n=10):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.lower_sum(function_of_x, a, b, n))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Lower sum of " + function_of_x + " on [" + str(a) + ", " + str(b) + "] with " + str(n) + " subintervals:")), file=discord_file)

@client.command()
async def disk_method(ctx, function="", variable_of_integration="x", a="0", b="1", line_of_rotation="0"):
    if (is_input_bad([function, variable_of_integration, a, b, line_of_rotation])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.disk_method(function, variable_of_integration, a, b, line_of_rotation))
    discord_file = img_to_discord(im)
    if (variable_of_integration == "x"):
        opposite_variable_of_integration = "y"
    else:
        opposite_variable_of_integration = "x"
    await ctx.send((code_blockify("Disk method of " + function + " on [" + str(a) + ", " + str(b) + "] about " + opposite_variable_of_integration + "=" + str(line_of_rotation))), file=discord_file)

@client.command()
async def washer_method(ctx, function1="", function2="", variable_of_integration="x", a="0", b="1", line_of_rotation="0"):
    if (is_input_bad([function1, function2, variable_of_integration, a, b, line_of_rotation])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.washer_method(function1, function2, variable_of_integration, a, b, line_of_rotation))
    discord_file = img_to_discord(im)
    if (variable_of_integration == "x"):
        opposite_variable_of_integration = "y"
    else:
        opposite_variable_of_integration = "x"
    await ctx.send((code_blockify("Washer method of " + function1 + " and " + function2 + " on [" + str(a) + ", " + str(b) + "] about " + opposite_variable_of_integration + "=" + str(line_of_rotation))), file=discord_file)
    
"""
How to use:
If it rotates about a y=, then the variable of integration is "y" (dy).
If it rotates about an x=, then the variable of integration is "x" (dx).
The thing it rotates about is the line of rotation (default is 0).
a and b are the bounds of integration (find the intersects to decide what to pass for a and b)
function2 is the possible second function given to you. This is typically a line. You can recognize it by finding anything else that says opposite of variable of integration=a function.
Example problem:
Use the method of cylindrical shells to find the volume V generated by rotating the region bounded by the given curves about y = 8.
64y=x^3
y=0
x=8
Using the command:
Note that we are rotating about y=8 which means that the variable of integration is y and our line_of_rotation is 8.
Since our variable of integration is y, we must find 64y=x^3 in terms of x. x=4y^(1/3)
y=0 is in terms of y (our variable of integration), so it must be one of our bounds. Our other bound can be found by substituting x=8 into our function to find that our other bound is y=8.
Thus, a and b are 0 and 8, respectively.
Note that we are given x=8, which is in terms of x, which is the opposite of our variable of integration. That means that we must pass it as our function2
!shell_method 4y^(1/3) y 0 8 8 8
Gives us the output 1280pi/7, which is correct.
"""
@client.command() 
async def shell_method(ctx, function1="", variable_of_integration="x", a="0", b="1", line_of_rotation="0", function2="0"):
    if (is_input_bad([function1, variable_of_integration, a, b, line_of_rotation, function2])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.shell_method(function1, variable_of_integration, a, b, line_of_rotation, function2))
    discord_file = img_to_discord(im)
    if (function2 != 0):
        message = "Shell method of " + function1 + " and " + function2 + " on [" + str(a) + ", " + str(b) + "] about " + variable_of_integration + "=" + str(line_of_rotation)
    else:
        message = "Shell method of " + function1 + " on [" + str(a) + ", " + str(b) + "] about " + variable_of_integration + "=" + str(line_of_rotation)
    await ctx.send((code_blockify(message)), file=discord_file)

@client.command()
async def trapezoid_approximation(ctx, function="", a="0", b="1", n=10, variable_of_integration="x"):
    if (is_input_bad([function, a, b])):
        await ctx.send("Bad input")
        return
    if (n > 250):
        n = 250
    if (n < 0):
        n = 10
    exact_approx, float_approx = math_evaluations.trapezoid_approximation(function, a, b, n, variable_of_integration)
    im = math_evaluations.image_processing(exact_approx)
    discord_file = img_to_discord(im)
    message = "Trapezoid approximation of " + function + " on the interval [" + a + ", " + b + "] with " + str(n) + " subintervals: " + str(float_approx)
    await ctx.send((code_blockify(message)), file=discord_file)

@client.command()
async def trapezoid_rule(ctx, function="", a="0", b="1", n=10, variable_of_integration="x"):
    await trapezoid_approximation(ctx, function, a, b, n, variable_of_integration)

@client.command()
async def simpson_rule(ctx, function="", a="0", b="1", n=10, variable_of_integration="x"):
    if (is_input_bad([function, a, b])):
        await ctx.send("Bad input")
        return
    if (n > 250):
        n = 250
    if (n % 2 == 1):
        n += 1
    if (n < 0):
        n = 10
    exact_approx, float_approx = math_evaluations.simpson_rule(function, a, b, n, variable_of_integration)
    im = math_evaluations.image_processing(exact_approx)
    discord_file = img_to_discord(im)
    message = "Simpson's rule of " + function + " on the interval [" + a + ", " + b + "] with " + str(n) + " subintervals: " + str(float_approx)
    await ctx.send((code_blockify(message)), file=discord_file)

@client.command()
async def simpson_approximation(ctx, function_of_x="", a="0", b="1", n=10, variable_of_integration="x"):
    await simpson_rule(ctx, function_of_x, a, b, n, variable_of_integration)

@client.command()
async def arc_length(ctx, function="", a="0", b="1", variable_of_integration="x"):
    if (is_input_bad([function, a, b])): # variable_of_integration is never parsed
        await ctx.send("Bad input")
        return
    ans = math_evaluations.arc_length(function, a, b, variable_of_integration)
    im = math_evaluations.image_processing(ans[0])
    discord_file = img_to_discord(im)
    message = "Arc length of " + function + " on the interval [" + a + ", " + b + "]: "
    if ans[1] != None:
        message = message + "Estimated " + str(ans[1])
    await ctx.send((code_blockify(message)), file=discord_file)

@client.command()
async def euler_method(ctx, differential_equation="y+x", initial_x=0.0, initial_y=0.0, step_size = 0.1, n=5):
    if (is_input_bad([differential_equation])):
        await ctx.send("Bad input")
        return
    ans_list = math_evaluations.euler_method(differential_equation, initial_x, initial_y, step_size, n)
    message = "Euler's method of " + differential_equation + " with initial point of (" + str(initial_x) + ", " + str(initial_y) + "), step size of " + str(step_size) + " with " + str(n) + " iterations: "
    message += "\n" + str(ans_list)
    await ctx.send(code_blockify(message))

@client.command()
async def differentiate(ctx, function_of_x=""):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.differentiate(function_of_x))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Differentiate: " + function_of_x)), file=discord_file)

@client.command()
async def point_differentiate(ctx, function_of_x="", c=0.0):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.point_differentiate(function_of_x, c))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Derivative of " + function_of_x + " at x=" + str(c) + ":")), file=discord_file)

@client.command()
async def maximum_val(ctx, function_of_x="", a=0.0, b=1.0):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.maximum_val(function_of_x, a, b))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Maximum value of " + function_of_x + " on [" + str(a) + ", " + str(b) + "]:")), file=discord_file)

@client.command()
async def minimum_val(ctx, function_of_x="", a=0.0, b=1.0):
    if (is_input_bad([function_of_x])):
        await ctx.send("Bad input")
        return
    im = math_evaluations.image_processing(math_evaluations.minimum_val(function_of_x, a, b))
    discord_file = img_to_discord(im)
    await ctx.send((code_blockify("Minimum value of " + function_of_x + " on [" + str(a) + ", " + str(b) + "]:")), file=discord_file)

@client.command()
async def resources(ctx):
    embed = nextcord.Embed()
    embed.description = "Resources:"
    embed.description = embed.description + "\n[Khan Academy](https://www.khanacademy.org/)"
    embed.description = embed.description + "\n[Organic Chemistry Tutor YouTube](https://www.youtube.com/channel/UCEWpbFLzoYGPfuWUMFPSaoA/)"
    embed.description = embed.description + "\n[Professor Leonard YouTube](https://www.youtube.com/@ProfessorLeonard)"
    embed.description = embed.description + "\n[Paul's Online Notes](https://tutorial.math.lamar.edu/)"
    embed.description = embed.description + "\n[A Compilation of Useful, Free, Online Math Resources](https://www.reddit.com/r/math/comments/2mkmk0/a_compilation_of_useful_free_online_math_resources/)"
    embed.description = embed.description + "\n[Math 1A Doc](https://docs.google.com/document/d/1LHGV1RHbks3Us5upMeK4Ou3ti7E7i77rHiuSHulT1iA/edit?usp=sharing)"
    embed.description = embed.description + "\n[De Anza Student Success Center's Math, Science & Technology Resource Center](https://www.deanza.edu/studentsuccess/mstrc/)"
    embed.description = embed.description + "\n[De Anza's Math Performance Success Program](https://www.deanza.edu/mps/)"
    embed.description = embed.description + "\n[De Anza's Math, Engineering and Science Achievement Program](https://www.deanza.edu/mesa/)"
    embed.description = embed.description + "\n[Math 10 Videos](https://www.ocf.berkeley.edu/~parran/math10videos.html)"
    embed.description = embed.description + "\n[Math 1A Videos](https://www.ocf.berkeley.edu/~parran/math1avideos.html)"
    embed.description = embed.description + "\n[Math 1B Videos](https://www.ocf.berkeley.edu/~parran/math1bvideos.html)"
    embed.description = embed.description + "\n[Math 1C Videos](https://www.ocf.berkeley.edu/~parran/math1cvideos.html)"
    embed.description = embed.description + "\n[Math 1D Videos](https://www.ocf.berkeley.edu/~parran/math1dvideos.html)"
    embed.description = embed.description + "\n[Math 2A Videos](https://www.ocf.berkeley.edu/~parran/math2avideos.html)"
    embed.description = embed.description + "\n[Math 2B Videos](https://www.ocf.berkeley.edu/~parran/math2bvideos.html)"
    await ctx.send(embed=embed)

"""@client.slash_command(name = "hello", description = "Bot says hello", guild_ids = [server_id])
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello there! I am the math meme bot.")"""

client.run(TOKEN)