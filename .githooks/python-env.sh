# Общая часть хуков: находит рабочий Python (с установленным PyYAML) и задаёт UTF-8. Подключается командой `. .githooks/python-env.sh`.
# В Windows `python` нередко оказывается заглушкой Microsoft Store (она ничего не запускает), поэтому каждый вариант
# проверяется настоящим запуском: python3, python, затем лаунчер `py -3`.

export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

PY=""
for candidate in "python3" "python" "py -3"; do
  if $candidate -c "import yaml" >/dev/null 2>&1; then
    PY="$candidate"
    break
  fi
done

if [ -z "$PY" ]; then
  echo "Хук git не нашёл Python с модулем PyYAML (пробовали: python3, python, py -3)." >&2
  echo "Установите Python 3.10+ и выполните: python -m pip install -r scripts/requirements.txt" >&2
  echo "Если Python уже установлен, добавьте его в PATH (в Windows — отключите заглушки в «Параметры → Приложения → Псевдонимы выполнения приложений»)." >&2
  exit 1
fi
