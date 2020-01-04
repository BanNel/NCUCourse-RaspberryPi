# Magic Mirror (Emotion Detection) on Raspberry Pi
:::info
This is a Course Project, which based on IOT Technique.
**Course**: Internet of Things Practical (IM5032)
**Author**: Pokémon Masters
:::

:::danger
⚠️ The code in this project is based on several author. For the detail, please check the references.
:::


## :elephant:  Overview
It is a Magic Mirror (Emotion Detection), which can detect **user’s emotion** and **give some feedback (Quote)**.

| Screen | User's Control Panel |
| -------- | -------- | 
| ![](https://i.imgur.com/0vsOqRt.png)     | ![](https://i.imgur.com/76eY6jc.png)     | 


## :ideograph_advantage: Usage
This Project has two part: Screen Side and Control Side.

The magic mirror have three kinds of mode, **Real Mirror mode**, **Camera mode** and another is the **Encourage Quote mode**.

### Screen Side
| Running Mode | Description |
| -------- | -------- |
| **Real Mirror mode**     | Display the black background on screen, to pretend as the mirror.     |
| **Camera mode**     |  Show the real time camera on the screen | 
| **Encourage Quote mode**     | It can detect user’s emotion and give some encourage quote.     |

### Control Side (control by Website)
| Feature | Description |
| -------- | -------- |
| **Control Running mode**     | Change the Mode On Screen     |
| **Monitor Camera**     |  Show the real time camera via website | 

### Hardware
* Raspberry Pi Model 3B
* Wi-Fi
* Monitor (Screen)
* Intel® Neural Compute Stick 2 (Intel® NCS2)
* One Way Vision Glass Sticker (optional)
### Software
* Python 3.7
* Open-Vino (4.1.2-openvino)


## :confetti_ball: Code Reference
:::success
Thanks for all the Source, without you I couldn't make it perfect.
:::


### Website Templates
* http://www.mashup-template.com/preview.html?template=energy

### Pi Camera on Flask (Real time)
* https://www.pyimagesearch.com/2016/01/18/multiple-cameras-with-the-raspberry-pi-and-opencv/
### Emotion Detection on Raspberry Pi

* https://chtseng.wordpress.com/2019/04/13/%E5%A6%82%E4%BD%95%E5%9C%A8%E6%A8%B9%E8%8E%93%E6%B4%BE%EF%BC%8Bncs%E4%BA%8C%E4%BB%A3%E4%BD%BF%E7%94%A8model-zoo%E5%8F%8A%E8%87%AA%E5%B7%B1%E8%A8%93%E7%B7%B4%E7%9A%84%E6%A8%A1%E5%9E%8B/#h2
* https://github.com/PINTO0309/OpenVINO-EmotionRecognition


## :cactus: Research Reference
* Richman, L. S., Kubzansky, L., Maselko, J., Kawachi, I., Choo, P., & Bauer, M. (2005). Positive emotion and health: going beyond the negative. Health psychology, 24(4), 422.
*  Tsujita, H., & Rekimoto, J. (2011, September). Smiling makes us happier: enhancing positive mood and communication with smile-encouraging digital appliances. In Proceedings of the 13th international conference on Ubiquitous computing (pp. 1-10). ACM.
*  Moore, G., Galway, L., & Donnelly, M. (2017, May). Remember to smile: design of a mobile affective technology to help promote individual happiness through smiling. In Proceedings of the 11th EAI International Conference on Pervasive Computing Technologies for Healthcare (pp. 348-354). ACM.
