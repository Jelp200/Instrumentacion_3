<div>
  <img src="../../assets/imgs/01 - MCE/header.png"/>
</div>

# MEDIDOR DE CALIDAD DE LA ENERGÍA :zap:

El siguiente instrumento permite medir la calidad de la energía de una linea de tensión de `127VRMS` a `60Hz` tambien denominada `Señal Pura`, la cual está siendo distorsionada por cinco diferentes señales con frecuencías y amplitudes distintas una de la otra `Señales de distorsión` . El panel principal de dicho instrumento es el siguiente:

<div><img src="/assets/imgs/01 - MCE/FP_1.png"></div>

Es posible observar que el instrumento permite ingresar para cada una de las señales de distorción una frecuencía y amplitud, esto con la finalidad de que se pueda probar la calidad de la señal en diferentes circunstancías, para poder conocer la frecuencía con la cuál trabajará cada una de estas señales de distorción es importante conocer la siguiente formula:

$$ f_{\text{señalDistorsion}} = f_{\text{fundamental}} \times nArmonico $$

Esto ya que para poder conocer la calidad de la energía se necesita trabajar con armonicos y sus frecuencias respectivas. Las amplitudes las cuales pueden ser ingresadas están dadas gracias a la siguiente tabla la cual es una relación de porcentajes con el voltaje `RMS` máximo de la señal de línea.

| **_Porcentaje (%)_** | **_Amplitud (V)_** |
|----------------------|--------------------|
| 3                    | 5.37               |
| 4                    | 7.16               |
| 5                    | 8.95               |
| 6                    | 10.74              |
| 7                    | 12.53              |
| 8                    | 14.32              |
| 9                    | 16.11              |
| 10                   | 17.9               |
| 11                   | 19.69              |
| 12                   | 21.48              |

Cómo ejemplo, se trabajarán con los primeros cinco armonicos y amplitudes vistas en la tabla, por lo tanto:

$$ f_{\text{SD1}} = 60 \times 2 = 120 | A_{\text{SD1}} = 5.37V$$
$$ f_{\text{SD2}} = 60 \times 3 = 180 | A_{\text{SD2}} = 7.16V$$
$$ f_{\text{SD3}} = 60 \times 4 = 240 | A_{\text{SD3}} = 8.95V$$
$$ f_{\text{SD4}} = 60 \times 5 = 300 | A_{\text{SD4}} = 10.74V$$
$$ f_{\text{SD5}} = 60 \times 6 = 360 | A_{\text{SD5}} = 12.53V$$

<div><img src="/assets/imgs/01 - MCE/FP_2.png"></div>

