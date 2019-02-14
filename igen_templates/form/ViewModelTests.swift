@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    
    private var disposeBag: DisposeBag!
    
    {% for p in properties %}
    private let {{ p.name }}Trigger = PublishSubject<{{ p.type.name }}>()
    {% endfor %}

    private let loadTrigger = PublishSubject<Void>()
    private let {{ submit }}Trigger = PublishSubject<Void>()
    private let cancelTrigger = PublishSubject<Void>()
    
    private var {{ model_variable }}: {{ model_name }}!
    
    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        {{ model_variable }} = {{ model_name }}()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_variable }})
        
        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
        {% for p in properties %}
            {{ p.name }}Trigger: {{ p.name }}Trigger.asDriverOnErrorJustComplete(),
        {% endfor %}
            {{ submit }}Trigger: {{ submit }}Trigger.asDriverOnErrorJustComplete(),
            cancelTrigger: cancelTrigger.asDriverOnErrorJustComplete()
        )
        
        output = viewModel.transform(input)
        
        disposeBag = DisposeBag()

        {% for p in properties %}
        output.{{ p.name }}.drive().disposed(by: disposeBag)
        {% endfor %}
        {% for p in properties %}
        output.{{ p.name }}Validation.drive().disposed(by: disposeBag)
        {% endfor %}
        output.{{ submit }}Enabled.drive().disposed(by: disposeBag)
        output.{{ submit }}.drive().disposed(by: disposeBag)
        output.cancel.drive().disposed(by: disposeBag)
        output.error.drive().disposed(by: disposeBag)
        output.loading.drive().disposed(by: disposeBag)
    }
    
    func test_loadTriggerInvoked_show{{ model_name }}() {
        // act
        loadTrigger.onNext(())
        {% for p in properties %}
        let {{ p.name }} = try? output.{{ p.name }}.toBlocking(timeout: 1).first()
        {% endfor %}
        
        // assert
        {% for p in properties %}
        XCTAssertEqual({{ p.name }}, {{ model_variable }}.{{ p.name }})
        {% endfor %}
    }
    
    func test_loadTriggerInvoked_enable_{{ submit }}_byDefault() {
        // act
        loadTrigger.onNext(())
        let {{ submit }}Enabled = try? output.{{ submit }}Enabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssertEqual({{ submit }}Enabled, true)
    }
    
    {% for p in properties %}
    func test_{{ p.name }}TriggerInvoked_validate{{ p.name_title }}() {
        // act
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {{ submit }}Trigger.onNext(())
        
        // assert
        XCTAssert(useCase.validate{{ p.name_title }}Called)
    }
    
    func test_{{ p.name }}TriggerInvoked_validate{{ p.name_title }}FailNotEnable_{{ submit }}() {
        // arrange
        useCase.validate{{ p.name_title }}ReturnValue = ValidationResult.invalid([TestError()])
        
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        let {{ submit }}Enabled = try? output.{{ submit }}Enabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssertEqual({{ submit }}Enabled, false)
    } {{ '\n' if not loop.last }}
    {% endfor %}
    
    func test_enable_{{ submit }}() {
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        let {{ submit }}Enabled = try? output.{{ submit }}Enabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssertEqual({{ submit }}Enabled, true)
    }
    
    func test_{{ submit }}TriggerInvoked_not_{{ submit }}() {
        // arrange
        {% if properties %}
        useCase.validate{{ properties[0].name_title }}ReturnValue = ValidationResult.invalid([TestError()])
        {% endif %}

        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        
        // assert
        XCTAssertFalse(useCase.{{ submit }}Called)
    }
    
    func test_{{ submit }}TriggerInvoked_{{ submit }}() {
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        
        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssert(navigator.dismissCalled)
    }
    
    func test_{{ submit }}TriggerInvoked_{{ submit }}FailShowError() {
        // arrange
        let {{ submit }}ReturnValue = PublishSubject<Void>()
        useCase.{{ submit }}ReturnValue = {{ submit }}ReturnValue
        
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        {{ submit }}ReturnValue.onError(TestError())
        let error = try? output.error.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssertFalse(navigator.dismissCalled)
        XCTAssert(error is TestError)
    }
    
    func test_cancelTriggerInvoked_dismiss() {
        // act
        cancelTrigger.onNext(())
        
        // assert
        XCTAssert(navigator.dismissCalled)
    }
    
}