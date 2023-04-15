#!/usr/bin/env python

import gradio as gr

from utils import randomize_seed_fn


def create_demo(process, max_images=12, default_num_images=3):
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                image = gr.Image()
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button('Run')
                with gr.Accordion('Advanced options', open=False):
                    num_samples = gr.Slider(label='Number of images',
                                            minimum=1,
                                            maximum=max_images,
                                            value=default_num_images,
                                            step=1)
                    image_resolution = gr.Slider(label='Image resolution',
                                                 minimum=256,
                                                 maximum=512,
                                                 value=512,
                                                 step=256)
                    canny_low_threshold = gr.Slider(
                        label='Canny low threshold',
                        minimum=1,
                        maximum=255,
                        value=100,
                        step=1)
                    canny_high_threshold = gr.Slider(
                        label='Canny high threshold',
                        minimum=1,
                        maximum=255,
                        value=200,
                        step=1)
                    num_steps = gr.Slider(label='Number of steps',
                                          minimum=1,
                                          maximum=100,
                                          value=20,
                                          step=1)
                    guidance_scale = gr.Slider(label='Guidance scale',
                                               minimum=0.1,
                                               maximum=30.0,
                                               value=9.0,
                                               step=0.1)
                    seed = gr.Slider(label='Seed',
                                     minimum=0,
                                     maximum=1000000,
                                     step=1,
                                     value=0,
                                     randomize=True)
                    randomize_seed = gr.Checkbox(label='Randomize seed',
                                                 value=True)
                    a_prompt = gr.Textbox(
                        label='Additional prompt',
                        value='best quality, extremely detailed')
                    n_prompt = gr.Textbox(
                        label='Negative prompt',
                        value=
                        'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'
                    )
            with gr.Column():
                result = gr.Gallery(label='Output', show_label=False).style(
                    columns=2, object_fit='scale-down')
        inputs = [
            image,
            prompt,
            a_prompt,
            n_prompt,
            num_samples,
            image_resolution,
            num_steps,
            guidance_scale,
            seed,
            canny_low_threshold,
            canny_high_threshold,
        ]
        prompt.submit(
            fn=randomize_seed_fn,
            inputs=[seed, randomize_seed],
            outputs=seed,
        ).then(
            fn=process,
            inputs=inputs,
            outputs=result,
        )
        run_button.click(
            fn=randomize_seed_fn,
            inputs=[seed, randomize_seed],
            outputs=seed,
        ).then(
            fn=process,
            inputs=inputs,
            outputs=result,
            api_name='canny',
        )
    return demo


if __name__ == '__main__':
    from model import Model
    model = Model(task_name='Canny')
    demo = create_demo(model.process_canny)
    demo.queue().launch()
