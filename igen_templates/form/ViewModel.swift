import Dto
import MGArchitecture
import RxCocoa
import RxSwift

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModel
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<Void>
        {% for p in properties %}
        let {{ p.name }}Trigger: Driver<{{ p.type.name }}>
        {% endfor %}
        let {{ submit }}Trigger: Driver<Void>
        let cancelTrigger: Driver<Void>
    }

    struct Output {
        {% for p in properties %}
        @Property var {{ p.name }} = {{ p.type.default_value }}
        {% endfor %}
        {% for p in properties %}
        @Property var {{ p.name }}Validation = ValidationResult.success(())
        {% endfor %}
        @Property var is{{ submit_title }}Enabled = true
        @Property var error: Error?
        @Property var isLoading = false
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()

        // Error
        
        let errorTracker = ErrorTracker()
        
        errorTracker
            .asDriver()
            .drive(output.$error)
            .disposed(by: disposeBag)

        // Loading
        
        let activityIndicator = ActivityIndicator()
        
        activityIndicator.asDriver()
            .drive(output.$isLoading)
            .disposed(by: disposeBag)

        // Properties

        {% for p in properties %}
        input.loadTrigger
            .map { self.{{ model_variable }}.{{ p.name }} }
            .drive(output.${{ p.name }})
            .disposed(by: disposeBag){{ '\n' if not loop.last }}
        {% endfor %}

        // Validations
        
        {% for p in properties %}
        let {{ p.name }}Validation = Driver.combineLatest(
                input.{{ p.name }}Trigger,
                input.{{ submit }}Trigger
            )
            .map { $0.0 }
            .map { {{ p.name }} -> ValidationResult in
                self.useCase.validate({{ p.name }}: {{ p.name }})
            }

        {{ p.name }}Validation
            .drive(output.${{ p.name }}Validation)
            .disposed(by: disposeBag){{ '\n' if not loop.last }}
        {% endfor %}

        // Actions

        let is{{ submit_title }}Enabled = Driver.and(
            {% for p in properties %}
            {{ p.name }}Validation.map { $0.isValid }{{ ',' if not loop.last }}
            {% endfor %}
        )
        .startWith(true)

        is{{ submit_title }}Enabled
            .drive(output.$is{{ submit_title }}Enabled)
            .disposed(by: disposeBag)

        input.{{ submit }}Trigger
            .withLatestFrom(is{{ submit_title }}Enabled)
            .filter { $0 }
            .withLatestFrom(Driver.combineLatest(
                {% for p in properties %}
                input.{{ p.name }}Trigger{{ ',' if not loop.last }}
                {% endfor %}
            ))
            .flatMapLatest { params -> Driver<{{ model_name }}> in
                let ({% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %}) = params
                let {{ model_variable }} = self.{{ model_variable }}.with {
                    {% for p in properties %}
                    $0.{{ p.name }} = {{ p.name }}
                    {% endfor %}
                }
                return self.useCase.{{ submit }}({{ model_variable }})
                    .trackError(errorTracker)
                    .trackActivity(activityIndicator)
                    .asDriverOnErrorJustComplete()
                    .map { _ in {{ model_variable }} }
            }
            .drive(onNext: { {{ model_variable }} in
                self.navigator.dismiss()
            })
            .disposed(by: disposeBag)

        input.cancelTrigger
            .drive(onNext: navigator.dismiss)
            .disposed(by: disposeBag)

        return output
    }
}