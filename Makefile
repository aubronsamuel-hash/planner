.PHONY: bootstrap up down test fmt lint monitoring

bootstrap:
	./scripts/sh/init_repo.sh

up:
	./scripts/sh/dev_up.sh

down:
	./scripts/sh/dev_down.sh

test:
	./scripts/sh/run_tests.sh

fmt:
	./scripts/sh/fmt.sh

lint:
	./scripts/sh/lint.sh

monitoring:
	./scripts/sh/dev_monitoring.sh
