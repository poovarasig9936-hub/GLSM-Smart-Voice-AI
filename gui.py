import tkinter as tk
import threading

from assistant_core import process_command
from error_explainer import explain_error

from voice_input import listen
from voice_output import speak


# Text Input Function

def send_message():

    command = entry.get()

    if command.strip() == "":
        return


    chat_box.insert(
        "end",
        "You: " + command + "\n"
    )


    try:

        response = process_command(command)


        chat_box.insert(
            "end",
            "AI: " + str(response) + "\n\n"
        )


        chat_box.see(tk.END)


        threading.Thread(
            target=speak,
            args=(str(response),),
            daemon=True
        ).start()


    except Exception as e:

        explanation = explain_error(str(e))


        chat_box.insert(
            "end",
            "AI Error Explanation:\n"
            + explanation
            + "\n\n"
        )


    entry.delete(
        0,
        tk.END
    )



# Voice Function

def speak_command():

    # Listening message

    chat_box.insert(
        "end",
        "Listening...\n\n"
    )

    chat_box.see(tk.END)
    chat_box.update()


    command = listen()


    if command:


        chat_box.insert(
            "end",
            "You: " + command + "\n"
        )


        try:


            response = process_command(command)


            chat_box.insert(
                "end",
                "AI: " + str(response) + "\n\n"
            )


            chat_box.see(tk.END)


            threading.Thread(
                target=speak,
                args=(str(response),),
                daemon=True
            ).start()



        except Exception as e:


            explanation = explain_error(str(e))


            chat_box.insert(
                "end",
                "AI Error Explanation:\n"
                + explanation
                + "\n\n"
            )



# Window

root = tk.Tk()


root.title(
    "GLSM AI - Voice Based Coding Assistant"
)


root.geometry(
    "700x500"
)



# Chat Box

chat_box = tk.Text(
    root,
    height=20,
    width=80
)


chat_box.pack(
    pady=10
)



chat_box.insert(
    "end",
    "Welcome to GLSM AI\n"
    "Voice Based Coding Assistant\n\n"
)



# Entry Box

entry = tk.Entry(
    root,
    width=60
)


entry.pack()



# Send Button

send_button = tk.Button(
    root,
    text="Send",
    command=send_message
)


send_button.pack(
    pady=5
)



# Voice Button

voice_button = tk.Button(
    root,
    text="🎤 Speak",
    command=lambda: threading.Thread(
        target=speak_command,
        daemon=True
    ).start()
)


voice_button.pack(
    pady=5
)



root.mainloop()
