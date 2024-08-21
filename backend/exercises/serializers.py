from rest_framework import serializers
from .models import Test, Answer, Question, QuestionVotes, TestVotes


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content', 'content_img_url', 'is_correct', 'id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_is_correct', False):
            representation.pop('is_correct', None)
        return representation


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        # fields = ['tests', 'statement', 'statement_img_url', 'author', 'route', 'created_at', 'subject', 'answers']
        fields = "__all__"

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance

        context = self.context.copy()
        context['exclude_is_correct'] = True
        serializer = AnswerSerializer(instance.answers.all(), many=True, context=context)
        representation = super().to_representation(instance)
        representation['answers'] = serializer.data

        return representation

    def create(self, validated_data):
        answer_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)

        for answer in answer_data:
            Answer.objects.create(question=question, **answer)

        return question


class TestSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = "__all__"


class QuestionVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionVotes
        fields = '__all__'


class TestVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestVotes
        fields = '__all__'

