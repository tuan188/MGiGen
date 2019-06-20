    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
        {% for p in input_properties %}
            {{ p.name }}: Driver.empty(){{ ',' if not loop.last }}
        {% endfor %}
        )

        let output = viewModel.transform(input)

    {% for p in output_properties %}
        output.{{ p.name }}
              .drive()
              .disposed(by: rx.disposeBag){{ '\n' if not loop.last }}
    {% endfor %}
    }