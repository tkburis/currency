import tkinter as tk
from tkinter import ttk
import rates
import grapher


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Exchange Rates')

        self.paddings = {'padx': 5, 'pady': 5}

        self.currency_options = rates.get_all_currencies()

        self.quit_button = ttk.Button(self, text="Quit", command=self._quit)
        self.quit_button.grid(row=0, sticky=tk.E)

        self.create_exchange_frame()
        ttk.Separator(self, orient='horizontal').grid(row=2, sticky=tk.EW)
        self.create_graphing_frame()

    def create_exchange_frame(self) -> None:
        exchange_frame = ttk.Frame(self)
        exchange_frame.grid(row=1)

        currency_from = tk.StringVar(self)
        currency_to = tk.StringVar(self)

        input_exchange_var = tk.StringVar(self)
        output_exchange_var = tk.StringVar(self)

        ttk.Label(exchange_frame, text='Live Currency Conversion').grid(row=0)

        input_entry = ttk.Entry(exchange_frame, textvariable=input_exchange_var)
        input_entry.grid(row=1, column=0, sticky=tk.W, **self.paddings)

        currency_from_drop = ttk.OptionMenu(exchange_frame, currency_from, *self.currency_options)
        currency_from_drop.grid(row=1, column=1, sticky=tk.W, **self.paddings)
        currency_from.set(self.currency_options[0])

        ttk.Label(exchange_frame, text=' to ').grid(row=1, column=2)

        currency_to_drop = ttk.OptionMenu(exchange_frame, currency_to, *self.currency_options)
        currency_to_drop.grid(row=1, column=3, sticky=tk.W, **self.paddings)
        currency_to.set(self.currency_options[1])

        def calculate_exchange():
            self.calculate_exchange(currency_from.get(), currency_to.get(), input_exchange_var, output_exchange_var)

        exchange_button = ttk.Button(exchange_frame, text='Go', command=calculate_exchange)
        exchange_button.grid(row=2, column=2, sticky=tk.W, **self.paddings)

        output_entry = ttk.Entry(exchange_frame, foreground='red', textvariable=output_exchange_var)
        output_entry.grid(row=1, column=4, sticky=tk.W, **self.paddings)

        return

    def create_graphing_frame(self) -> None:
        graphing_frame = ttk.Frame(self)
        graphing_frame.grid(row=3)

        graph_currency_from = tk.StringVar(self)
        graph_currency_to = tk.StringVar(self)
        time_span = tk.StringVar(self)

        ttk.Label(graphing_frame, text='Generate Rate Graph').grid(row=0, columnspan=3)

        ttk.Label(graphing_frame, text='Graph').grid(row=1, column=0)

        currency_from_drop = ttk.OptionMenu(graphing_frame, graph_currency_from, *self.currency_options)
        currency_from_drop.grid(row=1, column=1, sticky=tk.W, **self.paddings)
        graph_currency_from.set(self.currency_options[0])

        ttk.Label(graphing_frame, text=' to ').grid(row=1, column=2)

        currency_to_drop = ttk.OptionMenu(graphing_frame, graph_currency_to, *self.currency_options)
        currency_to_drop.grid(row=1, column=3, sticky=tk.W, **self.paddings)
        graph_currency_to.set(self.currency_options[1])

        ttk.Label(graphing_frame, text=' over   ').grid(row=1, column=4)

        time_span_entry = ttk.Entry(graphing_frame, textvariable=time_span)
        time_span_entry.grid(row=1, column=5, sticky=tk.W, **self.paddings)

        ttk.Label(graphing_frame, text=' months').grid(row=1, column=6)

        def get_graph():
            self.get_graph(graph_currency_from.get(), graph_currency_to.get(), time_span.get())

        graph_button = ttk.Button(graphing_frame, text='Graph', command=get_graph)
        graph_button.grid(row=2, column=3)

        return

    @staticmethod
    def get_input(input_var) -> float:
        try:
            _input = float(input_var.get())
        except ValueError:
            _input = 0
        return _input

    def calculate_exchange(self, currency_from, currency_to, _input, output) -> None:
        value = self.get_input(_input)
        converted = rates.convert_currency(currency_from, currency_to, value=value)
        output.set(f'{converted:.2f} {currency_to}')
        return

    @staticmethod
    def get_graph(currency_from, currency_to, time_span):
        try:
            time_span = int(time_span)
        except ValueError:
            time_span = 60
        graph = grapher.Grapher(time_span)
        graph.make_graph(currency_from, currency_to)

    def _quit(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()
