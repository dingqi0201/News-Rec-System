#!/bin/sh
  
for max_click_history in 1
do
	for max_hot_news in 5 6 7 1 2
	do
		for n in 0 1 2 3 4 5 6 7
		do
			echo "max_click_history = $max_click_history, max_hot_news= $max_hot_news, 第 $n 次训练正在执行... \n"
			python main.py --max_click_history $max_click_history --max_hot_news $max_hot_news
		done
	done
done
echo "执行完毕！"

