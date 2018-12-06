final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    private var disposeBag: DisposeBag!

{% for p in input_properties %}
    private let {{ p.name }} = PublishSubject<{{ p.type_name }}>()
{% endfor %}

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)
        
        input = {{ name }}ViewModel.Input(
        {% for p in input_properties %}
            {{ p.name }}: {{ p.name }}.asDriverOnErrorJustComplete(){{ "," if not loop.last }}
        {% endfor %}
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

    {% for p in output_properties %}
        output.{{ p.name }}.drive().disposed(by: disposeBag)
    {% endfor %}
    }
    
{% for p in input_properties %}
    func test_{{ p.name }}_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

{% endfor %}
}